# -*- coding: utf-8 -*-
from bms.v1.action import Action


class DeleteStratigraphy(Action):

    async def execute(self, id):
        await self.conn.fetchval("""
                DELETE FROM public.stratigraphy
                WHERE id_sty = $1
            """, id)
        return None
