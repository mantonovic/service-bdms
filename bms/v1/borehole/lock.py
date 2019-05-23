# -*- coding: utf-8 -*-
from bms.v1.borehole.get import GetBorehole
from bms import Locked
from datetime import datetime
from datetime import timedelta


class Lock(GetBorehole):

    async def execute(self, id, user_id):

        now = datetime.now()

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
