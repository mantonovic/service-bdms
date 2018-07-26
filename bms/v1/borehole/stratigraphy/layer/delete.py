# -*- coding: utf-8 -*-
from bms.v1.action import Action


class DeleteLayer(Action):

    async def execute(self, id):
        await self.conn.fetchval("""
            DELETE FROM public.layer
            WHERE id_lay = $1
        """, id)
