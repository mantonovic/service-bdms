# -*- coding: utf-8 -*-
from bms.v1.borehole.get import GetBorehole
from bms import Locked
from datetime import datetime
from datetime import timedelta


class StartEditing(GetBorehole):

    async def execute(self, id, user_id):

        # Lock row for current user
        await self.conn.execute("""
            UPDATE borehole SET
                locked_at = current_timestamp,
                locked_by = $1
            WHERE id_bho = $2;
        """, user_id, id)

        # return borehole data
        return await super().execute(id, True)
