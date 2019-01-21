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
                    depth_to_lay as depth_to,
                    CASE
                        WHEN elevation_z_bho is NULL THEN NULL
                        ELSE elevation_z_bho - depth_from_lay
                    END AS msm_from,
                    CASE
                        WHEN elevation_z_bho is NULL THEN NULL
                        ELSE elevation_z_bho - depth_to_lay
                    END AS msm_to,
                    lithostratigraphy_id_cli as lithostratigraphy,
                    layer.lithology_id_cli as lithology
                    /*,
                    SUM(depth_to_lay)
                        OVER (ORDER BY depth_from_lay, id_lay ASC) AS depth*/
                FROM
                    layer, stratigraphy, borehole
                WHERE
                    id_sty_fk = $1
                AND
                    id_sty = id_sty_fk
                AND
                    id_bho_fk = id_bho
                ORDER BY depth_from_lay, id_lay
            ) AS t
        """, id)
        return {
            "data": self.decode(rec[0]) if rec[0] is not None else []
        }
