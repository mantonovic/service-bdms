# -*- coding: utf-8 -*-
from bms.v1.action import Action


class CreateBorehole(Action):

    async def execute(self, user_id):
        return {
            "id": (
                await self.conn.fetchval("""
                    INSERT INTO public.borehole(author_id)
                    VALUES ($1) RETURNING id_bho
                """, user_id)
            )
        }
