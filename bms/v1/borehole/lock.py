# -*- coding: utf-8 -*-
from bms.v1.borehole.get import GetBorehole
from bms import Locked
from datetime import datetime
from datetime import timedelta


class Lock(GetBorehole):

    async def execute(self, id, user_id):

        now = datetime.now()
        rec = await self.conn.fetchrow("""
            SELECT
                locked_at,
                locked_by,
                firstname || ' ' || lastname
            FROM
                borehole
            LEFT JOIN users
              ON users.id_usr = borehole.locked_by
            WHERE
                id_bho = $1
        """, id)

        if rec is None:
            raise Exception(f"Borehole with id: '{id}' not exists")

        locked_at = rec[0]
        locked_by = rec[1]
        locked_by_name = rec[2]

        
        td = timedelta(minutes=self.lock_timeout)

        # Check if not locked
        if (
            locked_at is not None and  # Locked by someone
            locked_by != user_id and   # Someone is not the current user
            (now - locked_at) < (td)   # Timeout not finished
        ):
            raise Locked(
                id,
                {
                    "user": locked_by_name,
                    "datetime": locked_at.isoformat()
                }
            )

        # Lock row for current user
        await self.conn.execute("""
            UPDATE borehole SET
                locked_at = $1,
                locked_by = $2
            WHERE id_bho = $3;
        """, now, user_id, id)

        res = await self.conn.fetchval("""
            SELECT row_to_json(t2)
            FROM (
                SELECT
                    borehole.locked_by as id,
                    locker.username as username,
                    locker.firstname || ' ' || locker.lastname
                        as fullname,
                    to_char(
                        borehole.locked_at,
                        'YYYY-MM-DD"T"HH24:MI:SS'
                    ) as date
                FROM
                    borehole
                INNER JOIN public.users as locker
                    ON locked_by = locker.id_usr
                WHERE id_bho = $1
            ) t2
        """, id)

        return {
            "data": self.decode(res) if res is not None else None
        }
