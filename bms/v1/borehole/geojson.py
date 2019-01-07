# -*- coding: utf-8 -*-
from bms.v1.action import Action


class ListGeojson(Action):

    async def execute(self, filter={}):

        params = []
        where = []

        self.idx = 0

        def getIdx():
            self.idx += 1
            return "$%s" % self.idx

        if 'identifier' in filter.keys() and filter['identifier'] != '':
            params.append("%%%s%%" % filter['identifier'])
            where.append("""
                original_name_bho ILIKE %s
            """ % getIdx())

        if 'kind' in filter.keys() and filter['kind'] != None:
            params.append(int(filter['kind']))
            where.append("""
                kind_id_cli = %s
            """ % getIdx())

        if 'restriction' in filter.keys() and filter[
                'restriction'] != None:
            params.append(int(filter['restriction']))
            where.append("""
                restriction_id_cli = %s
            """ % getIdx())

        wr = ''
        if len(where) > 0:
            wr = """
                AND %s
            """ % " AND ".join(where)

        print("""
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
                                                        as public_name,
                                                    kind_id_cli
                                                        as kind,
                                                    original_name_bho
                                                        as original_name,
                                                    length_bho
                                                        as length
                                            ) AS p
                                        ) AS properties
                                    FROM borehole
                                    WHERE geom_bho IS NOT NULL
                                    AND geom_bho && ST_MakeEnvelope (
                                        2420000, 1030000,
                                        2900000, 1350000,
                                        2056
                                    )
                                    %s
                                ) f
                            ), '{}'::json[]
                        ) AS features
                ) t
        """ % (wr))

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
                                                        as public_name,
                                                    kind_id_cli
                                                        as kind,
                                                    original_name_bho
                                                        as original_name,
                                                    length_bho
                                                        as length
                                            ) AS p
                                        ) AS properties
                                    FROM borehole
                                    WHERE geom_bho IS NOT NULL
                                    AND geom_bho && ST_MakeEnvelope (
                                        2420000, 1030000,
                                        2900000, 1350000,
                                        2056
                                    )
                                    %s
                                ) f
                            ), '{}'::json[]
                        ) AS features
                ) t
        """ % (wr), *(params))
        return {
            "data": self.decode(rec[0])
        }
