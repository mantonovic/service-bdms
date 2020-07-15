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
            'username': 'guest',
            'viewer': True,
            'admin': False,
            'roles': ['VIEW'],
            'name': 'Guest User',
            'setting': {
                "defaults": {
                    "stratigraphy": 3002
                },
                "filter": {},
                "efilter": {},
                "boreholetable": {
                    "orderby": "original_name",
                    "direction": "ASC"
                },
                "eboreholetable": {
                    "orderby": "creation",
                    "direction": "DESC"
                },
                "map": {
                    "explorer": {},
                    "editor": {}
                },
                "appearance": {
                    "explorer": 1
                }
            },
            'terms': False,
            'workgroups': [],
            'wid': []

        }

    async def prepare(self):

        auth_header = self.request.headers.get('Authorization')
        auth_type = self.request.headers.get('bdms-authorization', False)

        if auth_header is None or not auth_header.startswith('Basic '):

            self.set_header('WWW-Authenticate', 'Basic realm=BDMS')
            self.set_status(401)
            self.finish()
            return

        auth_decoded = base64.decodestring(auth_header[6:].encode('utf-8'))
        username, password = auth_decoded.decode('utf-8').split(':', 2)

        # Permit guest login
        if (
            username == 'guest'
            and password == 'MeiSe0we1Oowief'
        ):
            pass

        else:

            async with self.pool.acquire() as conn:

                val = await conn.fetchval("""
                    SELECT row_to_json(t)
                    FROM (
                        SELECT
                            id_usr as "id",
                            username,
                            COALESCE(tr.terms, FALSE) terms,
                            COALESCE(
                                viewer_usr, FALSE
                            ) as viewer,
                            COALESCE(
                                admin_usr, FALSE
                            ) as admin,
                            firstname || ' ' || lastname as "name",
                            COALESCE(
                                settings_usr::json,
                                value_cfg::json
                            ) as setting,
                            COALESCE(
                                w.ws, '[]'::json
                            ) AS workgroups,
                            COALESCE(
                                w.wgps, '{}'::int[]
                            ) AS wid,
                            COALESCE(
                                rl.roles, '{}'::character varying[]
                            ) AS roles
                        FROM
                            bdms.users

                        INNER JOIN bdms.config
                        ON name_cfg = 'SETTINGS'

                        LEFT JOIN (
                            SELECT
                                r.id_usr_fk,
                                array_agg(r.name_rol) AS roles
                            FROM (
                                SELECT distinct
                                    id_usr_fk,
                                    name_rol
                                FROM
                                    bdms.users_roles,
                                    bdms.roles,
                                    bdms.workgroups
                                WHERE
                                    id_rol = id_rol_fk
                                AND
                                    id_wgp = id_wgp_fk
                            ) r
                            GROUP BY id_usr_fk
                        ) as rl
                        ON rl.id_usr_fk = id_usr

                        LEFT JOIN (
                            SELECT
                                id_usr_fk,
                                TRUE as terms
                            FROM
                                bdms.terms_accepted
                            INNER JOIN
                                bdms.terms
                            ON
                                id_tes_fk = id_tes
                            WHERE
                                expired_tes IS NULL
                            AND
                                draft_tes IS FALSE
                        ) as tr
                        ON
                            tr.id_usr_fk = id_usr

                        LEFT JOIN (
                            SELECT
                                id_usr_fk,
                                array_agg(id_wgp) as wgps,
                                array_to_json(array_agg(j)) as ws
                            FROM (
                                SELECT
                                    id_usr_fk,
                                    id_wgp,
                                    json_build_object(
                                        'id', id_wgp,
                                        'workgroup', name_wgp,
                                        'roles', array_agg(name_rol),
                                        'disabled', disabled_wgp
                                    ) as j
                                FROM
                                    bdms.users_roles,
                                    bdms.workgroups,
                                    bdms.roles
                                WHERE
                                    id_rol = id_rol_fk
                                AND
                                    id_wgp_fk = id_wgp
                                GROUP BY
                                    id_usr_fk,
                                    id_wgp
                                ORDER BY
                                    name_wgp
                            ) AS t
                            GROUP BY id_usr_fk
                        ) as w
                        ON w.id_usr_fk = id_usr

                        WHERE
                            username = $1
                        AND
                            password = crypt($2, password)
                        AND
                            disabled_usr IS NULL
                    ) as t
                """, username, password)

                if val is None:

                    if auth_type == 'bdms-v1':
                        self.write({
                            "success": False,
                            "message": "Authentication error",
                            "error": "E-102"
                        })

                    else:
                        self.set_header(
                            'WWW-Authenticate',
                            'Basic realm=BDMS'
                        )
                        self.set_status(401)

                    self.finish()
                    return

                self.user = json.loads(val)

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

            self.write({
                **{"success": True},
                **response
            })

        except BmsException as bex:
            print(traceback.print_exc())
            self.write({
                "success": False,
                "message": str(bex),
                "error": bex.code,
                "data": bex.data
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
