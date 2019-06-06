# -*- coding: utf-8 -*-
from bms.v1.borehole.get import GetBorehole
from bms import Locked


class Unlock(GetBorehole):

    async def execute(self, id):

        # Lock row for current user
        await self.conn.execute("""
            UPDATE borehole SET
                locked_at = NULL,
                locked_by = NULL
            WHERE id_bho = $1;
        """, id)

        return {}
