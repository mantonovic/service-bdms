# -*- coding: utf-8 -*-
from bms import (
    AuthorizationException,
    BaseHandler,
    EDIT,
    Locked
)
from bms.v1.borehole import (
    Lock
)
from datetime import datetime
from datetime import timedelta


class Producer(BaseHandler):

    async def check_lock(self, id, user, conn):
        rec = await conn.fetchrow("""
            SELECT
                locked_at,
                locked_by,
                firstname || ' ' || lastname,
                status[array_length(status, 1)]  ->> 'role' as "role",
                borehole.id_wgp_fk

            FROM
                borehole

            INNER JOIN (
                SELECT
                    id_bho_fk,
                    array_agg(
                        json_build_object(
                            'workflow', id_wkf,
                            'role', name_rol,
                            'username', username,
                            'started', started,
                            'finished', finished
                        )
                    ) as status
                FROM (
                    SELECT
                        id_bho_fk,
                        name_rol,
                        id_wkf,
                        username,
                        started_wkf as started,
                        finished_wkf as finished
                    FROM
                        workflow,
                        roles,
                        users
                    WHERE
                        id_rol = id_rol_fk
                    AND
                        id_usr = id_usr_fk
                    ORDER BY
                        id_wkf
                ) t
                GROUP BY
                    id_bho_fk
            ) as v
            ON
                v.id_bho_fk = id_bho

            LEFT JOIN
                users
            ON
                users.id_usr = borehole.locked_by

            WHERE
                id_bho = $1
        """, id)

        if rec is None:
            raise Exception(f"Borehole with id: '{id}' not exists")

        # Lockable by editors if borehole belong to user
        # group and borehole role is same as user's

        workgroup = None
        for wg in user['workgroups']:
            if wg['id'] == rec[4]:
                workgroup = wg

        if workgroup is None or rec[3] not in workgroup['roles']:
            raise AuthorizationException()

        now = datetime.now()

        td = timedelta(minutes=Lock.lock_timeout)

        locked_at = rec[0]
        locked_by = rec[1]
        locked_by_name = rec[2]

        if (
            locked_at is not None and     # Locked by someone
            locked_by != user['id'] and   # Someone is not the current user
            (now - locked_at) < (td)      # Timeout not finished
        ):
            raise Locked(
                id, 
                {
                    "user": locked_by_name,
                    "datetime": locked_at.isoformat()
                }
            )

        # Lock row for current user
        # await conn.execute("""
        #     UPDATE borehole SET
        #         locked_at = $1,
        #         locked_by = $2
        #     WHERE id_bho = $3;
        # """, now, user['id'], id)

    def authorize(self):

        if (
            'EDIT' in self.user['roles'] or
            'CONTROL' in self.user['roles'] or
            'VALID' in self.user['roles'] or
            'PUBLIC' in self.user['roles']
        ):
            return

        raise AuthorizationException()
