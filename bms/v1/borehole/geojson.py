# -*- coding: utf-8 -*-
from bms.v1.action import Action


class ListGeojson(Action):

    async def execute(self, filter={}, user=None):

        permissions = None
        if user is not None:
            permissions = self.filterPermission(user)

        where, params = self.filterBorehole(filter)

        wr = ''
        if len(where) > 0:
            wr = """
                AND %s
            """ % " AND ".join(where)

        if permissions is not None:
            wr += """
                AND {}
            """.format(
                permissions
            )

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
                                                    kd.code_cli
                                                        as kind_code,
                                                    rs.code_cli
                                                        as restriction_code,
                                                    original_name_bho
                                                        as original_name,
                                                    length_bho
                                                        as length
                                            ) AS p
                                        ) AS properties

                                    FROM bdms.borehole

                                    INNER JOIN (
                                        SELECT
                                            id_bho_fk,
                                            array_agg(
                                                json_build_object(
                                                    'workflow', id_wkf,
                                                    'role', name_rol,
                                                    'username', username,
                                                    'started', started,
                                                    'finished', finished
                                                )
                                            ) as status
                                        FROM (
                                            SELECT
                                                id_bho_fk,
                                                name_rol,
                                                id_wkf,
                                                username,
                                                started_wkf as started,
                                                finished_wkf as finished
                                            FROM
                                                bdms.workflow,
                                                bdms.roles,
                                                bdms.users
                                            WHERE
                                                id_rol = id_rol_fk
                                            AND
                                                id_usr = id_usr_fk
                                            ORDER BY
                                                id_wkf
                                        ) t
                                        GROUP BY
                                            id_bho_fk
                                    ) as v
                                    ON
                                        v.id_bho_fk = id_bho

                                    LEFT JOIN
                                        bdms.codelist kd
                                    ON
                                        kind_id_cli = kd.id_cli

                                    LEFT JOIN
                                        bdms.codelist rs
                                    ON
                                        restriction_id_cli = rs.id_cli

                                    WHERE
                                        geom_bho IS NOT NULL
                                    AND
                                        geom_bho && ST_MakeEnvelope (
                                            2420000, 1030000,
                                            2900000, 1350000,
                                            2056
                                    )
                                    %s
                                ) f
                            ), '{}'::json[]
                        ) AS features
                ) t
        """ % wr, *(params))
        return {
            "data": self.decode(rec[0])
        }
