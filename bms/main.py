# -*- coding: utf-8 -*-
from tornado import web
from tornado.options import define, options
from tornado.platform.asyncio import AsyncIOMainLoop
import asyncio
import asyncpg
from tornado.httpserver import HTTPServer
import sys

sys.path.append('.')

define("port", default=8888, help="Tornado Web port", type=int)
define("pg_host", default="localhost", help="PostgrSQL database host")
define("pg_port", default="5432", help="PostgrSQL database port")
define("pg_database", default="bms", help="PostgrSQL database name")

async def get_conn():
    return await asyncpg.create_pool(
        user='postgres', password='postgres',
        database=options.pg_database, host=options.pg_host)

if __name__ == "__main__":

    options.parse_command_line()

    from bms import (
        # user handlers
        SettingHandler,
        UserHandler,

        # Borehole handlers
        BoreholeViewerHandler,
        BoreholeProducerHandler,
        # BoreholeExporterHandler,
        ExportHandler,

        # Stratigraphy handlers
        StratigraphyHandler,

        # Layer handlers
        LayerViewerHandler,
        LayerProducerHandler,

        # Other handlers
        GeoapiHandler,
        ProjectHandler,
        CodeListHandler,
        MunicipalityHandler,
        CantonHandler,
        Wmts
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
        (r'/api/v1/user', UserHandler),

        # Borehole handlers
        (r'/api/v1/borehole', BoreholeViewerHandler),
        # (r'/api/v1/borehole/export', BoreholeExporterHandler),
        (r'/api/v1/borehole/edit', BoreholeProducerHandler),
        (r'/api/v1/borehole/download', ExportHandler),

        # Stratigraphy handlers
        (r'/api/v1/borehole/stratigraphy', StratigraphyHandler),

        # Layer handlers
        (r'/api/v1/borehole/stratigraphy/layer', LayerViewerHandler),
        (r'/api/v1/borehole/stratigraphy/layer/edit', LayerProducerHandler),

        # Other handlers
        (r'/api/v1/borehole/project', ProjectHandler),
        (r'/api/v1/borehole/codes', CodeListHandler),
        (r'/api/v1/geoapi/municipality', MunicipalityHandler),
        (r'/api/v1/geoapi/canton', CantonHandler),
        (r'/api/v1/geoapi/location', GeoapiHandler),
        (r"/api/v1/geoapi/wmts", Wmts)

    ], **settings)

    application.pool = ioloop.run_until_complete(get_conn())

    http_server = HTTPServer(application)
    http_server.listen(options.port, 'localhost')
    ioloop.run_forever()
