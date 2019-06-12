# -*- coding: utf-8 -*-
from bms import EDIT
from bms.v1.action import Action


class CreateBorehole(Action):

    async def execute(self, id, user):
        bid = await self.conn.fetchval("""
            INSERT INTO public.borehole(
                project_id,
                author_id,
                updater_bho,
                id_wgp_fk,
                id_rol_fk
            )
            VALUES (
                $1, $2, $3, $4, $5
            ) RETURNING id_bho
        """, id, user['id'], user['id'], user['workgroups'][0]['id'], EDIT)

        return {
            "id": bid
        }
