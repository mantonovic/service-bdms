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
                'viewer',
                'producer'
            ],
            'name': 'anonymous',
            'setting': {}
        }

    async def prepare(self):
        async with self.pool.acquire() as conn:
            rec = await conn.fetchrow("""
                SELECT
                    id_usr,
                    username,
                    settings_usr
                FROM
                    users
                WHERE id_usr = $1
            """, 1)
            self.user['id'] = rec[0]
            self.user['username'] = rec[1]
            self.user['name'] = rec[1]
            self.user['setting'] = (
                json.loads(rec[2]) if rec[2] is not None else {}
            )

    @property
    def pool(self):
        return self.application.pool

    @property
    def _user(self):
        auth_header = self.request.headers.get('Authorization')
        if auth_header is None or not auth_header.startswith('Basic '):
            return {
                'id': 1,
                'username': 'anonymous',
                'roles': [
                    'viewer',
                    'producer'
                ],
                'name': 'anonymous'
            }
        auth_decoded = base64.decodestring(auth_header[6:].encode('utf-8'))
        username, password = auth_decoded.decode('utf-8').split(':', 2)
        return {
            'id': 1,
            'username': username,
            'roles': [
                'viewer',
                'producer'
            ],
            'name': username
        }

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
