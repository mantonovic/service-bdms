# -*- coding: utf-8 -*-
from bms.v1.action import Action


class GetLayer(Action):

    async def execute(self, id, user=None):

        permission = ''

        if user is not None:
            permission = """
                AND {}
            """.format(
                self.filterPermission(user)
            )

        rec = await self.conn.fetchrow(f"""
            SELECT row_to_json(t)
            FROM (
                SELECT
                    id_lay AS id,
                    (
                        select row_to_json(t)
                        FROM (
                            SELECT
                                creator.id_usr as id,
                                creator.username as username,
                                to_char(
                                    creation_lay,
                                    'YYYY-MM-DD"T"HH24:MI:SS'
                                ) as date
                        ) t
                    ) as creator,
                    (
                        select row_to_json(t)
                        FROM (
                            SELECT
                                updater.id_usr as id,
                                updater.username as username,
                                to_char(
                                    update_lay,
                                    'YYYY-MM-DD"T"HH24:MI:SS'
                                ) as date
                        ) t
                    ) as updater,
                    depth_from_lay AS depth_from,
                    depth_to_lay AS depth_to,
                    COALESCE(
                        description_lay, ''
                    ) AS description,
                    COALESCE(
                        geology_lay, ''
                    ) AS geology,
                    last_lay AS last,
                    layer.qt_description_id_cli AS qt_description,
                    layer.lithology_id_cli AS lithology,
                    layer.lithostratigraphy_id_cli AS lithostratigraphy,
                    layer.chronostratigraphy_id_cli AS chronostratigraphy,
                    layer.tectonic_unit_id_cli AS tectonic_unit,
                    layer.symbol_id_cli AS symbol,
                    COALESCE(
                        mlpr112, '{{}}'::int[]
                    ) AS color,
                    layer.plasticity_id_cli AS plasticity,
                    layer.humidity_id_cli AS humidity,
                    layer.consistance_id_cli AS consistance,
                    layer.alteration_id_cli AS alteration,
                    layer.compactness_id_cli AS compactness,
                    COALESCE(
                        mlpr113, '{{}}'::int[]
                    ) AS jointing,
                    layer.soil_state_id_cli AS soil_state,
                    COALESCE(
                        mlpr108, '{{}}'::int[]
                    ) AS organic_component,
                    striae_lay AS striae,
                    layer.grain_size_1_id_cli AS grain_size_1,
                    layer.grain_size_2_id_cli AS grain_size_2,
                    COALESCE(
                        mlpr110, '{{}}'::int[]
                    ) AS grain_shape,
                    COALESCE(
                        mlpr115, '{{}}'::int[]
                    ) AS grain_granularity,
                    layer.cohesion_id_cli AS cohesion,
                    COALESCE(
                        mlpr117, '{{}}'::int[]
                    ) AS further_properties,
                    layer.uscs_1_id_cli AS uscs_1,
                    layer.uscs_2_id_cli AS uscs_2,
                    COALESCE(
                        mcla101, '{{}}'::int[]
                    ) AS uscs_3,
                    COALESCE(
                        uscs_original_lay, ''
                    ) AS uscs_original,
                    COALESCE(
                        mcla104, '{{}}'::int[]
                    ) AS uscs_determination,
                    -- layer.unconrocks_id_cli AS unconrocks,
                    COALESCE(
                        mcla107, '{{}}'::int[]
                    ) AS debris,
                    COALESCE(
                        vlit401, '{{}}'::int[]
                    ) AS lit_pet_deb,
                    lithok_id_cli AS lithok,
                    kirost_id_cli AS kirost,
                    unconrocks_id_cli AS unconrocks,
                    COALESCE(
                        notes_lay, ''
                    ) AS notes,
                    stratigraphy.kind_id_cli AS kind
                FROM
                    bdms.layer

                INNER JOIN bdms.stratigraphy as stratigraphy
                ON id_sty_fk = stratigraphy.id_sty

                INNER JOIN bdms.borehole
                ON stratigraphy.id_bho_fk = id_bho

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

                INNER JOIN bdms.users as creator
                ON creator_lay = creator.id_usr

                INNER JOIN bdms.users as updater
                ON updater_lay = updater.id_usr

                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as mlpr112
                    FROM
                        bdms.layer_codelist
                    WHERE
                        code_cli = 'mlpr112'
                    GROUP BY id_lay_fk
                ) clr
                ON clr.id_lay_fk = id_lay

                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as mlpr113
                    FROM
                        bdms.layer_codelist
                    WHERE
                        code_cli = 'mlpr113'
                    GROUP BY id_lay_fk
                ) jng
                ON jng.id_lay_fk = id_lay

                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as mlpr108
                    FROM
                        bdms.layer_codelist
                    WHERE
                        code_cli = 'mlpr108'
                    GROUP BY id_lay_fk
                ) oco
                ON oco.id_lay_fk = id_lay

                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as mlpr110
                    FROM
                        bdms.layer_codelist
                    WHERE
                        code_cli = 'mlpr110'
                    GROUP BY id_lay_fk
                ) gsh
                ON gsh.id_lay_fk = id_lay

                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as mlpr115
                    FROM
                        bdms.layer_codelist
                    WHERE
                        code_cli = 'mlpr115'
                    GROUP BY id_lay_fk
                ) ggr
                ON ggr.id_lay_fk = id_lay

                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as mlpr117
                    FROM
                        bdms.layer_codelist
                    WHERE
                        code_cli = 'mlpr117'
                    GROUP BY id_lay_fk
                ) ftp
                ON ftp.id_lay_fk = id_lay

                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as mcla101
                    FROM
                        bdms.layer_codelist
                    WHERE
                        code_cli = 'mcla101'
                    GROUP BY id_lay_fk
                ) us3
                ON us3.id_lay_fk = id_lay

                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as mcla104
                    FROM
                        bdms.layer_codelist
                    WHERE
                        code_cli = 'mcla104'
                    GROUP BY id_lay_fk
                ) usd
                ON usd.id_lay_fk = id_lay

                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as mcla107
                    FROM
                        bdms.layer_codelist
                    WHERE
                        code_cli = 'mcla107'
                    GROUP BY id_lay_fk
                ) dbr
                ON dbr.id_lay_fk = id_lay

                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as vlit401
                    FROM
                        bdms.layer_codelist
                    WHERE
                        code_cli = 'custom.lit_pet_top_bedrock'
                    GROUP BY id_lay_fk
                ) lpd
                ON lpd.id_lay_fk = id_lay

                WHERE id_lay = $1
                {permission}
            ) AS t
        """, id)
        return {
            "data": self.decode(rec[0]) if rec[0] is not None else None
        }
