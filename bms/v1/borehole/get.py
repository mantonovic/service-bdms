# -*- coding: utf-8 -*-
from bms.v1.action import Action


class GetBorehole(Action):

    async def execute(self, id):
        rec = await self.conn.fetchrow("""
            SELECT
                row_to_json(t)
            FROM (
                SELECT
                    id_brh as id,
                    name_brh as name
                FROM
                    boreholes
                WHERE id_brh = $1
            ) AS t
        """, id)
        return {
            "data": self.decode(rec[0]) if rec[0] is not None else None
        }
