# -*- coding: utf-8 -*-
from bms.v1.action import Action


class CreateLayer(Action):

    async def execute(self, id):
        return {
            "id": (
                await self.conn.fetchval("""
                    INSERT INTO public.layer(id_sty_fk)
                    VALUES ($1) RETURNING id_lay
                """, id)
            )
        }
