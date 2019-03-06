# -*- coding: utf-8 -*-
from tornado import web
import json
import traceback
import base64
from bms.v1.exceptions import (
    BmsException,
    AuthenticationException,
    ActionEmpty
)
# from bms.v1 import coroutine


class BaseHandler(web.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.user = {
            'id': 0,
            'username': 'anonymous',
            'roles': [
                'viewer', 'producer'
            ],
            'name': 'Pinco Pallina',
            'setting': {
                "filter": {
                    "custom": {
                        "project_name": True,
                        "landuse": True,
                        "public_name": True,
                        "canton": True,
                        "city": True
                    },
                    "restriction": True,
                    "mapfilter": True,
                    "restriction_until": True,
                    "extended": {
                        "original_name": True,
                        "method": True,
                        "status": True
                    },
                    "kind": True,
                    "elevation_z": True,
                    "length": True,
                    "drilling_date": True
                },
                "boreholetable": {
                    "orderby": "original_name",
                    "direction": "ASC"
                },
                "eboreholetable": {
                    "orderby": "creation",
                    "direction": "DESC"
                }
            }
        }

    async def prepare(self):
        async with self.pool.acquire() as conn:
            auth_header = self.request.headers.get('Authorization')
            if auth_header is None or not auth_header.startswith('Basic '):
                return self.user

            auth_decoded = base64.decodestring(auth_header[6:].encode('utf-8'))
            username, password = auth_decoded.decode('utf-8').split(':', 2)

            async with self.pool.acquire() as conn:
                rec = await conn.fetchrow("""
                    SELECT
                        id_usr,
                        username,
                        settings_usr
                    FROM
                        users
                    WHERE username = $1
                    AND password = $2
                """, username, password)
                self.user['id'] = rec[0]
                self.user['username'] = rec[1]
                self.user['name'] = rec[1]
                self.user['roles'] = ['viewer', 'producer']
                self.user['setting'] = (
                    json.loads(rec[2]) if rec[2] is not None else {}
                )

    @property
    def pool(self):
        return self.application.pool

    async def post(self, *args, **kwargs):
        try:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            if self.user is None:
                raise AuthenticationException()

            self.authorize()
            body = self.request.body.decode('utf-8')
            if body is None or body == '':
                raise ActionEmpty()

            response = await self.execute(
                json.loads(body)
            )

            if response is None:
                response = {}

            self.write(
                {
                    **{
                        "success": True
                    },
                    **response
                }
            )

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

    def authorize(self):
        pass

    async def get(self, *args, **kwargs):
        self.write("Method not supported")
        self.finish()

    async def execute(self, request):
        return {
            "message": "execute function not implemented"
        }
