# -*- coding: utf-8 -*-
from bms.v1.borehole.get import GetBorehole
from bms import Locked


class Unlock(GetBorehole):

    async def execute(self, id, user_id):

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

        # Check if locked by current user
        if (
            locked_by is not None and
            locked_by != user_id 
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
                locked_at = NULL,
                locked_by = NULL
            WHERE id_bho = $1;
        """, id)

        return {}
