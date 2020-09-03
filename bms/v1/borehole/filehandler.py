# -*- coding: utf-8 -*-
from tornado.options import options
from bms.v1.handlers import Producer
from bms.v1.borehole import (
    DetachFile,
    PatchFile
)
from io import StringIO
from io import BytesIO
import zipfile
import traceback
from bms.v1.exceptions import (
    BmsException,
    AuthorizationException,
    AuthenticationException,
    ActionEmpty,
    MissingParameter,
    NotFound
)
import json
import datetime
import boto3
from botocore.exceptions import ClientError
import uuid
import hashlib


class FileHandler(Producer):

    # Uploading files
    async def post(self, *args, **kwargs):
        if (
            'Content-Type' in self.request.headers and
            'multipart/form-data' in self.request.headers['Content-Type']
        ):
            try:
                self.set_header(
                    "Content-Type",
                    "application/json; charset=utf-8"
                )

                self.set_header("Content-Type", "application/json; charset=utf-8")
                if self.user is None:
                    raise AuthenticationException()

                self.authorize()

                s3 = None

                # Check file repository
                if options.file_repo == 's3':
                    session = boto3.Session(
                        aws_access_key_id=options.aws_access_key_id,
                        aws_secret_access_key=options.aws_secret_access_key,
                    )
                    s3 = session.resource('s3')

                async with self.pool.acquire() as conn:
                    try:
                        await conn.execute("BEGIN;")

                        borehole_id = int(self.get_body_argument('id'))

                        for files in self.request.files.items():

                            for info in files[1]:
                                file_body = BytesIO(info["body"])
                                file_name = info["filename"]

                                extension = ''
                                if file_name.find('.') > 0:
                                    extension = file_name.rsplit('.', 1)[1].lower()

                                file_type = info["content_type"]

                                # Calculating hash
                                m = hashlib.sha256()
                                m.update(info["body"])
                                file_hash = m.hexdigest()

                                # Check for file duplication
                                id_fil = await conn.fetchval(
                                    """
                                        SELECT
                                            id_fil
                                        FROM
                                            bdms.files
                                        WHERE
                                            hash_fil = $1
                                    """, file_hash
                                )

                                conf = {}

                                # upload to file repository if not exists
                                if id_fil is None:

                                    # store file
                                    if options.file_repo == 's3':

                                        # Giving a unig file name
                                        conf['key'] = "{}.{}".format(
                                            str(uuid.uuid1()), extension
                                        )

                                        try:
                                            s3.Bucket(
                                                options.aws_bucket
                                            ).upload_fileobj(
                                                file_body, conf['key'],
                                                ExtraArgs={
                                                    'Metadata': {
                                                        'filename': file_name
                                                    },
                                                    'ContentType': file_type
                                                }
                                            )

                                        except ClientError:
                                            print(traceback.print_exc())
                                            raise Exception(
                                                "Error while uploading to AWS"
                                            )

                                    # Insert info into database
                                    id_fil = await conn.fetchval(
                                        """
                                            INSERT INTO bdms.files (
                                                name_fil, hash_fil,
                                                type_fil, conf_fil,
                                                id_usr_fk
                                            ) VALUES (
                                                $1, $2, $3, $4, $5
                                            )
                                            RETURNING id_fil;
                                        """,
                                        file_name,
                                        file_hash,
                                        file_type,
                                        json.dumps(conf),
                                        self.user['id']
                                    )

                                # Attach file to borehole
                                await conn.execute(
                                    """
                                        INSERT INTO bdms.borehole_files (
                                            id_bho_fk, id_fil_fk, id_usr_fk
                                        ) VALUES (
                                            $1, $2, $3
                                        );
                                    """, borehole_id, id_fil, self.user['id']
                                )

                        await conn.execute("COMMIT;")

                    except Exception as ex:
                        print(traceback.print_exc())
                        await conn.execute("ROLLBACK;")
                        raise ex

                self.write({
                    "success": True
                })

            except Exception as ex:
                print(traceback.print_exc())
                self.write({
                    "success": False,
                    "message": str(ex)
                })

            self.finish()

        else:
            await super(
                FileHandler, self
            ).post(*args, **kwargs)


    async def get(self, *args, **kwargs):
        try:

            if self.user is None:
                raise AuthenticationException()

            self.authorize()

            self.set_header(
                "Expires",
                datetime.datetime.utcnow() +
                datetime.timedelta(seconds=1)
            )

            self.set_header(
                "Cache-Control",
                "max-age=" + str(1)
            )

            s3 = None

            # Check file repository
            if options.file_repo == 's3':
                session = boto3.Session(
                    aws_access_key_id=options.aws_access_key_id,
                    aws_secret_access_key=options.aws_secret_access_key,
                )
                s3 = session.resource('s3')

            async with self.pool.acquire() as conn:

                file_id = int(self.get_argument('id', 0))

                if file_id == 0:
                    raise NotFound()

                # Getting attachment info
                file_info = await conn.fetchrow("""
                    SELECT
                        name_fil,
                        type_fil,
                        conf_fil

                    FROM
                        bdms.files

                    WHERE
                        id_fil = $1
                """, file_id)

                if file_info is None:
                    raise NotFound()

                conf = json.loads(file_info[2])

                self.set_header("Content-Type", file_info[1])

                self.set_header(
                    "Content-Disposition",
                    f"inline; {file_info[0]}"
                )

                attachment = BytesIO()

                if options.file_repo == 's3':
                    
                    try:
                        s3.Bucket(
                            options.aws_bucket
                        ).download_fileobj(
                            conf['key'],
                            attachment
                        )

                    except ClientError:
                        print(traceback.print_exc())
                        raise Exception(
                            "Error while downloading from AWS"
                        )

                self.write(attachment.getvalue())

        except BmsException as bex:
            print(traceback.print_exc())
            self.write({
                "success": False,
                "message": str(bex),
                "error": bex.code
            })

        except Exception as ex:
            print(traceback.print_exc())
            self.write({
                "success": False,
                "message": str(ex)
            })

        self.finish()

    async def execute(self, request):

        action = request.pop('action', None)

        if action in [
            'DETACHFILE',
            'PATCH'
        ]:
            async with self.pool.acquire() as conn:

                exe = None

                # Lock check
                res = await self.check_lock(
                    request['id'], self.user, conn
                )

                if (
                    action in [
                        'DETACHFILE',
                        'PATCH'
                    ]
                ):
                    await self.check_edit(
                        request['id'], self.user, conn
                    )
                    if res['role'] != 'EDIT':
                        raise AuthorizationException() 

                if action == 'DETACHFILE':
                    exe = DetachFile(conn)
                    request['user'] = self.user

                elif action == 'PATCH':
                    exe = PatchFile(conn)
                    request['user'] = self.user

                request.pop('lang', None)

                if exe is not None:

                    ret = await exe.execute(**request)

                    if action == 'DETACHFILE':

                        # Check if the file is still linked to some
                        #  other borehole
                        val = await conn.fetchrow("""
                            SELECT
								COALESCE(cnt, 0) cnt,
                                conf_fil
                            FROM
                                bdms.files
                            LEFT JOIN (
                                SELECT
                                    id_fil_fk,
                                    COUNT(id_fil_fk) as cnt
                                FROM
                                    bdms.borehole_files
                                GROUP BY
                                    id_fil_fk
                            ) as cntr
                            ON
                                id_fil_fk = id_fil
                            WHERE
                                id_fil = $1
                        """, request['file_id'])

                        # If the file is unlinked from all boreholes then
                        #  delete it
                        if val[0] == 0:
                            await conn.execute("""
                                DELETE FROM
                                    bdms.files
                                WHERE
                                    id_fil = $1
                            """, request['file_id'])

                            s3 = None
                            conf = json.loads(val[1])

                            # Check file repository
                            if options.file_repo == 's3':
                                session = boto3.Session(
                                    aws_access_key_id=options.aws_access_key_id,
                                    aws_secret_access_key=options.aws_secret_access_key,
                                )
                                s3 = session.resource('s3')
                                
                            # Delete also the file from the file repository
                            if options.file_repo == 's3':
                            
                                try:
                                    s3.Bucket(
                                        options.aws_bucket
                                    ).delete_objects(
                                        Delete={
                                            'Objects': [
                                                {
                                                    'Key': conf['key']
                                                }
                                            ],
                                            'Quiet': True
                                        }
                                    )

                                except ClientError:
                                    print(traceback.print_exc())
                                    raise Exception(
                                        "Error while downloading from AWS"
                                    )

                    return ret

        raise Exception("Action '%s' unknown" % action)
