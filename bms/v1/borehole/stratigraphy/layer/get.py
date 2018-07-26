# -*- coding: utf-8 -*-
from bms.v1.action import Action


class GetLayer(Action):

    async def execute(self, id):
        rec = await self.conn.fetchrow("""
            SELECT row_to_json(t)
            FROM (
                SELECT
                    id_lay as id,
                    depth_from_lay as depth_from,
                    depth_to_lay as depth_to
                FROM
                    layer
                WHERE id_lay = $1
            ) AS t
        """, id)
        return {
            "data": self.decode(rec[0]) if rec[0] is not None else None
        }
