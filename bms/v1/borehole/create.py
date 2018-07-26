# -*- coding: utf-8 -*-
from bms.v1.action import Action


class CreateBorehole(Action):

    async def execute(self, id, user_id):
        return {
            "id": (
                await self.conn.fetchval("""
                    INSERT INTO public.borehole(
                        project_id, author_id)
                    VALUES ($1, $2) RETURNING id_bho
                """, id, user_id)
            )
        }
