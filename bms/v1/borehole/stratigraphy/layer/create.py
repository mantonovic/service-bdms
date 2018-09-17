# -*- coding: utf-8 -*-
from bms.v1.action import Action


class CreateLayer(Action):

    async def execute(self, id, user_id):
        # Check if there are other layers
        row = await self.conn.fetchrow("""
            SELECT
                depth_to_lay
            FROM
                layer
            WHERE
                id_sty_fk = $1
            ORDER BY depth_to_lay DESC
            LIMIT 1
        """, id)
        depth_to = 0
        if row is not None:
            depth_to = row[0]
        return {
            "id": (
                await self.conn.fetchval("""
                    INSERT INTO public.layer(
                        id_sty_fk, creator_lay,
                        updater_lay, depth_from_lay
                    )
                    VALUES ($1, $2, $3, $4) RETURNING id_lay
                """, id, user_id, user_id, depth_to)
            )
        }
