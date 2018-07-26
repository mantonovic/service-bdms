# -*- coding: utf-8 -*-
from bms.v1.action import Action


class ListLayers(Action):

    async def execute(self, id):
        rec = await self.conn.fetchrow("""
            SELECT
                array_to_json(
                    array_agg(
                        row_to_json(t)
                    )
                )
            FROM (
                SELECT
                    id_lay as id,
                    depth_from_lay as depth_from,
                    depth_to_lay as depth_to
                FROM
                    layer
                WHERE id_sty_fk = $1
                ORDER BY depth_from_lay, id_lay
            ) AS t
        """, id)
        return {
            "data": self.decode(rec[0]) if rec[0] is not None else []
        }
