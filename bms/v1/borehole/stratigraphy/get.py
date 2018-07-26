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
                    kind_id_cli as kind
                FROM
                    stratigraphy
                WHERE id_sty = $1
            ) AS t
        """, id)
        return {
            "data": self.decode(rec[0]) if rec[0] is not None else None
        }


'''
    rec = await self.conn.fetchrow("""
        SELECT
            row_to_json(t)
        FROM (
            SELECT
                id_sty as id,
                kind_id_cli as kind,
                (
                    select array_agg(row_to_json(t))
                    FROM (
                        SELECT
                            id_lay as id,
                            depth_from_lay as depth_from,
                            depth_to_lay as depth_to
                    ) t
                ) as layers
            FROM
                stratigraphy
            LEFT JOIN (
                SELECT
                    id_sty_fk,
                    array_agg(
                        row_to_json(
                            SELECT
                                id_lay as id,
                                depth_from_lay as depth_from,
                                depth_to_lay as depth_to
                        )
                    )
                FROM layer
            ) lay ON lay.id_sty_fk = id_sty
            WHERE id_sty = $1
        ) AS t
    """, id)
'''
