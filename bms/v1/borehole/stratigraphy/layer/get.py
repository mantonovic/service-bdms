# -*- coding: utf-8 -*-
from bms.v1.action import Action


class GetLayer(Action):

    async def execute(self, id):
        rec = await self.conn.fetchrow("""
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
                    qt_description_id_cli AS qt_description,
                    lithology_id_cli AS lithology,
                    lithostratigraphy_id_cli AS lithostratigraphy,
                    chronostratigraphy_id_cli AS chronostratigraphy,
                    tectonic_unit_id_cli AS tectonic_unit,
                    symbol_id_cli AS symbol,
                    COALESCE(
                        mlpr112, '{}'::int[]
                    ) AS color,
                    plasticity_id_cli AS plasticity,
                    humidity_id_cli AS humidity,
                    consistance_id_cli AS consistance,
                    alteration_id_cli AS alteration,
                    compactness_id_cli AS compactness,
                    COALESCE(
                        mlpr113, '{}'::int[]
                    ) AS jointing,
                    soil_state_id_cli AS soil_state,
                    COALESCE(
                        mlpr108, '{}'::int[]
                    ) AS organic_component,
                    striae_lay AS striae,
                    grain_size_1_id_cli AS grain_size_1,
                    grain_size_2_id_cli AS grain_size_2,
                    COALESCE(
                        mlpr110, '{}'::int[]
                    ) AS grain_shape,
                    COALESCE(
                        mlpr115, '{}'::int[]
                    ) AS grain_granularity,
                    cohesion_id_cli AS cohesion,
                    COALESCE(
                        mlpr117, '{}'::int[]
                    ) AS further_properties,
                    uscs_1_id_cli AS uscs_1,
                    uscs_2_id_cli AS uscs_2,
                    COALESCE(
                        mcla101, '{}'::int[]
                    ) AS uscs_3,
                    COALESCE(
                        uscs_original_lay, ''
                    ) AS uscs_original,
                    COALESCE(
                        mcla104, '{}'::int[]
                    ) AS uscs_determination,
                    unconrocks_id_cli AS unconrocks,
                    COALESCE(
                        mcla107, '{}'::int[]
                    ) AS debris,
                    COALESCE(
                        vlit401, '{}'::int[]
                    ) AS lit_pet_deb,
                    lithok_id_cli AS lithok,
                    kirost_id_cli AS kirost,
                    unconrocks_id_cli AS unconrocks,
                    COALESCE(
                        notes_lay, ''
                    ) AS notes,
                    kind_id_cli AS kind
                FROM
                    layer
                INNER JOIN public.stratigraphy as stratigraphy
                ON id_sty_fk = stratigraphy.id_sty
                INNER JOIN public.users as creator
                ON creator_lay = creator.id_usr
                INNER JOIN public.users as updater
                ON updater_lay = updater.id_usr
                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as mlpr112
                    FROM
                        layer_codelist
                    WHERE
                        code_cli = 'mlpr112'
                    GROUP BY id_lay_fk
                ) clr
                ON clr.id_lay_fk = id_lay
                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as mlpr113
                    FROM
                        layer_codelist
                    WHERE
                        code_cli = 'mlpr113'
                    GROUP BY id_lay_fk
                ) jng
                ON jng.id_lay_fk = id_lay
                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as mlpr108
                    FROM
                        layer_codelist
                    WHERE
                        code_cli = 'mlpr108'
                    GROUP BY id_lay_fk
                ) oco
                ON oco.id_lay_fk = id_lay
                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as mlpr110
                    FROM
                        layer_codelist
                    WHERE
                        code_cli = 'mlpr110'
                    GROUP BY id_lay_fk
                ) gsh
                ON gsh.id_lay_fk = id_lay
                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as mlpr115
                    FROM
                        layer_codelist
                    WHERE
                        code_cli = 'mlpr115'
                    GROUP BY id_lay_fk
                ) ggr
                ON ggr.id_lay_fk = id_lay
                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as mlpr117
                    FROM
                        layer_codelist
                    WHERE
                        code_cli = 'mlpr117'
                    GROUP BY id_lay_fk
                ) ftp
                ON ftp.id_lay_fk = id_lay
                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as mcla101
                    FROM
                        layer_codelist
                    WHERE
                        code_cli = 'mcla101'
                    GROUP BY id_lay_fk
                ) us3
                ON us3.id_lay_fk = id_lay
                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as mcla104
                    FROM
                        layer_codelist
                    WHERE
                        code_cli = 'mcla104'
                    GROUP BY id_lay_fk
                ) usd
                ON usd.id_lay_fk = id_lay
                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as mcla107
                    FROM
                        layer_codelist
                    WHERE
                        code_cli = 'mcla107'
                    GROUP BY id_lay_fk
                ) dbr
                ON dbr.id_lay_fk = id_lay
                LEFT JOIN (
                    SELECT
                        id_lay_fk, array_agg(id_cli_fk) as vlit401
                    FROM
                        layer_codelist
                    WHERE
                        code_cli = 'custom.lit_pet_top_bedrock'
                    GROUP BY id_lay_fk
                ) lpd
                ON lpd.id_lay_fk = id_lay
                WHERE id_lay = $1
            ) AS t
        """, id)
        return {
            "data": self.decode(rec[0]) if rec[0] is not None else None
        }
