# -*- coding: utf-8 -*-
from bms.v1.action import Action


class GetBorehole(Action):

    async def execute(self, id):
        rec = await self.conn.fetchrow("""
            SELECT
                row_to_json(t)
            FROM (
                SELECT
                    id_bho as id,
                    (
                        select row_to_json(t)
                        FROM (
                            SELECT
                                updater.id_usr as id,
                                updater.username as username,
                                to_char(
                                    update_bho,
                                    'YYYY-MM-DD"T"HH24:MI:SS'
                                ) as date
                        ) t
                    ) as updater,
                    (
                        select row_to_json(t2)
                        FROM (
                            SELECT
                                author.id_usr as id,
                                author.username as username,
                                to_char(
                                    created_bho,
                                    'YYYY-MM-DD"T"HH24:MI:SS'
                                ) as date
                        ) t2
                    ) as author,
                    kind_id_cli as kind,
                    restriction_id_cli as restriction,
                    to_char(
                        restriction_until_bho,
                        'YYYY-MM-DD'
                    ) as restriction_until,
                    location_x_bho as location_x,
                    location_y_bho as location_y,
                    srs_id_cli as srs,
                    qt_location_id_cli as qt_location,
                    elevation_z_bho as elevation_z,
                    hrs_id_cli as hrs,
                    qt_elevation_id_cli as qt_elevation,
                    drilling_date_bho as drilling_date,
                    bore_inc_bho as bore_inc,
                    bore_inc_dir_bho as bore_inc_dir,
                    length_bho as length,
                    (
                        select row_to_json(t)
                        FROM (
                            SELECT
                                COALESCE(
                                    original_name_bho, ''
                                ) as original_name,
                                method_id_cli as method,
                                purpose_id_cli as purpose,
                                status_id_cli as status,
                                top_bedrock_bho as top_bedrock,
                                groundwater_bho as groundwater
                        ) t
                    ) as extended,
                    (
                        select row_to_json(t)
                        FROM (
                            SELECT
                                COALESCE(
                                    name_pro, ''
                                ) as project_name,
                                COALESCE(
                                    public_name_bho, ''
                                ) as public_name,
                                canton_bho as canton,
                                city_bho as city,
                                address_bho as address,
                                landuse_id_cli as landuse,
                                cuttings_id_cli as cuttings,
                                drill_diameter_bho as drill_diameter,
                                qt_bore_inc_dir_id_cli as qt_bore_inc_dir,
                                qt_length_id_cli as qt_length,
                                qt_top_bedrock_id_cli as qt_top_bedrock,
                                COALESCE(
                                    alptb, '{}'::int[]
                                ) AS lit_pet_top_bedrock,
                                COALESCE(
                                    alstb, '{}'::int[]
                                ) AS lit_str_top_bedrock,
                                COALESCE(
                                    acstb, '{}'::int[]
                                ) AS chro_str_top_bedrock,
                                processing_status_id_cli
                                    as processing_status,
                                national_relevance_id_cli
                                    as national_relevance,
                                COALESCE(
                                    ate, '{}'::int[]
                                ) AS attributes_to_edit,
                                mistakes_bho as mistakes,
                                remarks_bho as remarks
                        ) t
                    ) as custom
                FROM
                    borehole
                INNER JOIN public.user as updater
                ON updater_bho = updater.id_usr
                INNER JOIN public.user as author
                ON author_id = author.id_usr
                LEFT JOIN project
                ON id_pro = project_id
                LEFT JOIN cantons
                ON kantonsnum = canton_bho
                LEFT JOIN municipalities
                ON municipalities.gid = city_bho
                LEFT JOIN (
                    SELECT
                        id_bho_fk, array_agg(id_cli_fk) as alptb
                    FROM
                        borehole_codelist
                    WHERE
                        code_cli = 'custom.lit_pet_top_bedrock'
                    GROUP BY id_bho_fk
                ) lptb
                ON lptb.id_bho_fk = id_bho
                LEFT JOIN (
                    SELECT
                        id_bho_fk, array_agg(id_cli_fk) as alstb
                    FROM
                        borehole_codelist
                    WHERE
                        code_cli = 'custom.lit_str_top_bedrock'
                    GROUP BY id_bho_fk
                ) lstb
                ON lstb.id_bho_fk = id_bho
                /*
https://jira.swisstopo.ch/browse/BMSWEB-14?focusedCommentId=59676
&page=com.atlassian.jira.plugin.system.issuetabpanels:comment-tabpanel
#comment-59676
                */
                LEFT JOIN (
                    SELECT
                        id_bho_fk, array_agg(id_cli_fk) as acstb
                    FROM
                        borehole_codelist
                    WHERE
                        code_cli = 'custom.chro_str_top_bedrock'
                    GROUP BY id_bho_fk
                ) cstb
                ON cstb.id_bho_fk = id_bho
                LEFT JOIN (
                    SELECT
                        id_bho_fk, array_agg(id_cli_fk) as ate
                    FROM
                        borehole_codelist
                    WHERE
                        code_cli = 'madm404'
                    GROUP BY id_bho_fk
                ) tmadm404
                ON tmadm404.id_bho_fk = id_bho
                WHERE id_bho = $1
            ) AS t
        """, id)

        print(id, rec)
        return {
            "data": self.decode(rec[0]) if rec[0] is not None else None
        }
