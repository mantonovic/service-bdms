# -*- coding: utf-8 -*-
"""This is the entry point to run the BDMS as a TornadoWeb service.
"""

__author__ = 'Institute of Earth science - SUPSI'
__version__ = '1.0.0'

from tornado import web
from tornado.options import define, options
from tornado.platform.asyncio import AsyncIOMainLoop
import asyncio
import asyncpg
from tornado.httpserver import HTTPServer
import sys
from pathlib import Path
import configparser

sys.path.append('.')

define("port", default=8888, help="Tornado Web port", type=int)
define("pg_user", default="postgres", help="PostgrSQL database user")
define("pg_password", default="postgres", help="PostgrSQL user password")
define("pg_host", default="localhost", help="PostgrSQL database host")
define("pg_port", default="5432", help="PostgrSQL database port")
define("pg_database", default="bms", help="PostgrSQL database name")
define("pg_upgrade", default=False, help="Upgrade PostgrSQL schema", type=bool)

define("file_repo", default='local', help="Select the file repository", type=str)

# Local storage for files configuration
define("local_path", default=str(Path.home()), help="Select local path", type=str)

# AWS S3 stzorage for files configuration
define("aws_bucket", default='bdms', help="Select AWS Bucket name", type=str)
define("aws_credentials", default=None, help="AWS S3 credential file location (overwrite aws_access_key_id and aws_secret_access_key)", type=str)
define("aws_access_key_id", default=None, help="AWS S3 access key id", type=str)
define("aws_secret_access_key", default=None, help="AWS S3 secret access key", type=str)

# Ordered list of available versions
versions = [
    "1.0.0",
    "1.0.1-RC1"
]

# SQL upgrades directory
udir = "./bms/assets/sql/"

# SQL to execute for upgrades
sql_files = {
    "1.0.0": f"{udir}1.0.0_to_1.0.1-RC1.sql"
}

async def get_conn():
    try:
        return await asyncpg.create_pool(
            user=options.pg_user,
            password=options.pg_password,
            database=options.pg_database,
            host=options.pg_host,
            port=options.pg_port
        )
    except Exception as x:
        red("Connection to db failed.")
        raise x


async def release_pool(pool):
    await pool.close()

def red(message):
    print(f"\033[91m{message}\033[0m")

def green(message):
    print(f"\033[92m{message}\033[0m")

def blue(message):
    print(f"\033[94m{message}\033[0m")

async def upgrade_database(pool):
    async with pool.acquire() as conn:
        try:
            await conn.execute("BEGIN;")
            current_db_version = await conn.fetchval("""
                SELECT
                    value_cfg
                FROM
                    bdms.config
                WHERE
                    name_cfg = 'VERSION';
            """)

            print("\nUpgrading database:")
            for idx in range(
                versions.index(current_db_version),
                len(versions)
            ):
                version = versions[idx]
                with open(sql_files[version]) as sql_file:
                    print(f" - Executing: {sql_files[version]}")
                    await conn.execute(sql_file.read())

            # Update current datetime of this upgrade
            await conn.execute("""
                UPDATE
                    bdms.config
                SET
                    value_cfg = to_char(
                        now(), 'YYYY-MM-DD"T"HH24:MI:SSOF'
                    )
                WHERE
                    name_cfg = 'PG_UPGRADE';
            """)

            # Update previous version
            await conn.execute("""
                UPDATE
                    bdms.config
                SET
                    value_cfg = $1
                WHERE
                    name_cfg = 'PREVIOUS';
            """, current_db_version)

            # Update current version
            await conn.execute("""
                UPDATE
                    bdms.config
                SET
                    value_cfg = $1
                WHERE
                    name_cfg = 'VERSION';
            """)

            await conn.execute("COMMIT;")

            print("Upgrading completed.")

        except Exception as ex:
            red("\n 😞 Sorry, an error occured during the upgrade process\n")
            await conn.execute("ROLLBACK;")
            raise ex

async def system_check(pool):
    async with pool.acquire() as conn:
        # Checking database version
        current_db_version = await conn.fetchval("""
            SELECT
                value_cfg
            FROM
                bdms.config
            WHERE
                name_cfg = 'VERSION';
        """)
    if current_db_version != __version__:
        from bms import DatabaseVersionMissmatch
        raise DatabaseVersionMissmatch(
            __version__,
            current_db_version
        )

if __name__ == "__main__":

    options.parse_command_line()

    from bms import (
        # Exceptions
        BmsDatabaseException,
        DatabaseVersionMissmatch,
        DatabaseUpgraded,
        DatabaseAlreadyUpgraded,

        # user handlers
        SettingHandler,
        DownloadHandler,
        UserHandler,
        AdminHandler,
        WorkgroupAdminHandler,

        # Borehole handlers
        BoreholeViewerHandler,
        BoreholeProducerHandler,
        # BoreholeExporterHandler,
        ExportHandler,
        FileHandler,

        # Identifier handlers
        IdentifierAdminHandler,
        IdentifierProducerHandler,
        IdentifierViewerHandler,

        # Stratigraphy handlers
        StratigraphyViewerHandler,
        StratigraphyProducerHandler,

        # Layer handlers
        LayerViewerHandler,
        LayerProducerHandler,

        # Workflow handlers
        WorkflowProducerHandler,

        # Other handlers
        GeoapiHandler,
        ProjectHandler,
        CodeListHandler,
        MunicipalityHandler,
        CantonHandler,
        Wmts,
        Wms,
        # GetFeature
    )

    AsyncIOMainLoop().install()
    ioloop = asyncio.get_event_loop()
    ioloop.set_debug(enabled=True)

    settings = dict(
        debug=True
    )

    application = web.Application([

        # Borehole handlers
        (r'/api/v1/setting', SettingHandler),
        (r'/api/v1/setting/download', DownloadHandler),
        (r'/api/v1/user', UserHandler),
        (r'/api/v1/user/edit', AdminHandler),

        (r'/api/v1/user/workgroup/edit', WorkgroupAdminHandler),

        # Borehole handlers
        (r'/api/v1/borehole', BoreholeViewerHandler),
        (r'/api/v1/borehole/edit', BoreholeProducerHandler),
        (r'/api/v1/borehole/download', ExportHandler),
        (r'/api/v1/borehole/edit/import', BoreholeProducerHandler),
        (r'/api/v1/borehole/edit/files', FileHandler),

        # Stratigraphy handlers
        (r'/api/v1/borehole/identifier', IdentifierViewerHandler),
        (r'/api/v1/borehole/identifier/edit', IdentifierProducerHandler),
        (r'/api/v1/borehole/identifier/admin', IdentifierAdminHandler),

        # Workflow handlers
        (r'/api/v1/workflow/edit', WorkflowProducerHandler),

        # Stratigraphy handlers
        (r'/api/v1/borehole/stratigraphy', StratigraphyViewerHandler),
        (r'/api/v1/borehole/stratigraphy/edit', StratigraphyProducerHandler),

        # Layer handlers
        (r'/api/v1/borehole/stratigraphy/layer', LayerViewerHandler),
        (r'/api/v1/borehole/stratigraphy/layer/edit', LayerProducerHandler),

        # Other handlers
        # (r'/api/v1/borehole/project', ProjectHandler),
        (r'/api/v1/borehole/codes', CodeListHandler),
        (r'/api/v1/geoapi/municipality', MunicipalityHandler),
        (r'/api/v1/geoapi/canton', CantonHandler),
        (r'/api/v1/geoapi/location', GeoapiHandler),
        (r"/api/v1/geoapi/wmts", Wmts),
        (r"/api/v1/geoapi/wms/swisstopo", Wms),
        # (r"/api/v1/geoapi/getfeature", GetFeature)

    ], **settings)

    application.pool = ioloop.run_until_complete(get_conn())

    if options.file_repo == 's3':

        if options.aws_credentials is None:
            raise Exception("AWS Credential file missing")
        
        config = configparser.ConfigParser()
        config.read(options.aws_credentials)

        if (
            'default' not in config or
            'aws_access_key_id' not in config['default'] or
            'aws_secret_access_key' not in config['default']
        ):
            raise Exception("AWS Credential wrong")

        options.aws_access_key_id = config['default']['aws_access_key_id']
        options.aws_secret_access_key = config['default']['aws_secret_access_key']

    try:
        # Check system before startup
#         try:
#             ioloop.run_until_complete(
#                 system_check(application.pool)
#             )

#             if options.pg_upgrade:
#                 raise DatabaseAlreadyUpgraded(__version__)

#         except DatabaseVersionMissmatch as dvm:

#             # Upgrade the database automatically
#             if options.pg_upgrade:
#                 answer = input("""
# You are going to upgrade your PostgreSQL schema.
# Be aware that this operation is not reversible.
# Before upgrading make sure you backup all your data.

# Do you wish to continue? [yes/no] """)

#                 if answer != "yes":
#                     raise dvm

#                 ioloop.run_until_complete(
#                     upgrade_database(application.pool)
#                 )

#                 raise DatabaseUpgraded(__version__)

#             else:
#                 raise dvm

        http_server = HTTPServer(application)
        http_server.listen(options.port)
        ioloop.run_forever()

#     except DatabaseVersionMissmatch as dvm:
#         print(f"""
# \033[91m{dvm}\033[0m

# Run this script with --pg-upgrade parameter
# to upgrade your database automatically.
# """)

    except BmsDatabaseException as du:
        print(f"\n 😃 \033[92m{du}\033[0m\n")

    except Exception as ex:
        print(f"Exception:\n{ex}")

    finally:
        ioloop.run_until_complete(release_pool(application.pool))
