# -*- coding: utf-8 -*-
from bms.v1.action import Action


class GetStratigraphy(Action):

    async def execute(self, id):
        rec = await self.conn.fetchrow("""
            SELECT
                row_to_json(t)
            FROM (
                SELECT
                    id_sty as id,
                    kind_id_cli as kind,
                    to_char(
                        date_sty,
                        'YYYY-MM-DD'
                    ) as date
                FROM
                    stratigraphy
                WHERE id_sty = $1
            ) AS t
        """, id)
        return {
            "data": self.decode(rec[0]) if rec[0] is not None else None
        }
