# -*- coding: utf-8 -*-
from bms.v1.borehole.get import GetBorehole
from bms import Locked
from datetime import datetime
from datetime import timedelta


class StartEditing(GetBorehole):

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

        minutes = 10
        td = timedelta(minutes=minutes)

        # Check if not locked
        if (
            locked_at is not None and  # Locked by someone
            locked_by != user_id and   # Someone is not the current user
            (now - locked_at) < (td)   # Timeout not finished
        ):
            raise Locked(
                id,
                {
                    "user": locked_by_name
                }
            )

        # Lock row for current user
        await self.conn.execute("""
            UPDATE borehole SET
                locked_at = current_timestamp,
                locked_by = $1
            WHERE id_bho = $2;
        """, user_id, id)

        # return borehole data
        return await super().execute(id, True)
