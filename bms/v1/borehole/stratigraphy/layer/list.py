# -*- coding: utf-8 -*-
from bms.v1.action import Action


class ListLayers(Action):

    async def execute(self, id, user=None):

        permissions = ''
        if user is not None:
            permissions = """
                AND {}
            """.format(
                self.filterPermission(user)
            )

        rec = await self.conn.fetchrow(f"""
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
                    layer

                INNER JOIN stratigraphy
                ON id_sty = id_sty_fk
                
                INNER JOIN borehole
                ON id_bho_fk = id_bho

                WHERE
                    id_sty_fk = $1

                {permissions}

                ORDER BY
                    depth_from_lay,
                    id_lay

            ) AS t
        """, id)

        return {
            "data": self.decode(rec[0]) if rec[0] is not None else []
        }
