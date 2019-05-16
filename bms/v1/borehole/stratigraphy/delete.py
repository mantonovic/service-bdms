# -*- coding: utf-8 -*-
from bms.v1.action import Action
from bms import Locked
from datetime import datetime
from datetime import timedelta


class DeleteStratigraphy(Action):

    async def execute(self, id, user_id):

        # First chehck if user has a lock on row
        rec = await self.conn.fetchrow("""
            SELECT
                locked_at,
                locked_by
            FROM
                borehole
            LEFT JOIN users
            ON users.id_usr = borehole.locked_by
            WHERE
                id_bho = $1
        """, id)

        if rec is not None:
            
            now = datetime.now()
            td = timedelta(minutes=self.lock_timeout)

            locked_at = rec[0]
            locked_by = rec[1]

            # Check if not locked or not locked by current user
            if (
                locked_by is None or
                (
                    locked_by != user_id
                    or (now - locked_at) > (td)
                )
            ):
                raise Locked(
                    id, None
                )

            await self.conn.fetchval("""
                    DELETE FROM public.stratigraphy
                    WHERE id_sty = $1
                """, id)

        return None
