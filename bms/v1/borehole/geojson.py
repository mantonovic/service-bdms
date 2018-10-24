# -*- coding: utf-8 -*-
from bms.v1.action import Action


class ListGeojson(Action):

    async def execute(self):
        rec = await self.conn.fetchrow("""
            SELECT
                row_to_json(t)
                FROM (
                    SELECT
                        'FeatureCollection' AS "type",
                        (
                            SELECT row_to_json(c)
                            FROM (
                                SELECT
                                    'name' AS "type",
                                    (
                                        SELECT row_to_json(p)
                                        FROM (
                                            SELECT
                                                'EPSG:2056' AS "name"
                                        ) AS p
                                    ) AS properties
                            ) c
                        ) AS crs,
                        COALESCE(
                            (
                                SELECT array_agg(row_to_json(f))
                                FROM (
                                    SELECT
                                        id_bho as id,
                                        'Feature' AS "type",
                                        ST_AsGeoJSON(
                                            geom_bho
                                        )::json AS "geometry",
                                        (
                                            SELECT row_to_json(p)
                                            FROM (
                                                SELECT
                                                    id_bho as id,
                                                    public_name_bho
                                                        as public_name
                                            ) AS p
                                        ) AS properties
                                    FROM borehole
                                    WHERE geom_bho IS NOT NULL
                                    AND geom_bho && ST_MakeEnvelope (
                                        2420000, 1030000,
                                        2900000, 1350000,
                                        2056
                                    )
                                ) f
                            ), '{}'::json[]
                        ) AS features
                ) t
        """)
        return {
            "data": self.decode(rec[0])
        }
