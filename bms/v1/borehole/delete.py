# -*- coding: utf-8 -*-
from bms.v1.action import Action


class DeleteBorehole(Action):

    async def execute(self, id):
        await self.conn.fetchval("""
                DELETE FROM bdms.borehole
                WHERE id_bho = $1
            """, id)
        return None
