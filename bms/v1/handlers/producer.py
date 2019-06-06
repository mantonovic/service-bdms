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
                borehole.id_rol_fk,
                borehole.id_grp_fk
            FROM
                borehole
            LEFT JOIN users
            ON users.id_usr = borehole.locked_by
            WHERE
                id_bho = $1
        """, id)

        if rec is None:
            raise Exception(f"Borehole with id: '{id}' not exists")

        # Lockable by editors if borehole belong to user
        # group and borehole role is same as user's
        if (
            rec[3] == EDIT and (
                rec[4] != user['group']['id'] or
                'EDIT' not in user['roles']
            )
        ):
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
        if 'EDIT' not in self.user['roles']:
            raise AuthorizationException()
