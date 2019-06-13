# -*- coding: utf-8 -*-
from bms.v1.action import Action


class GetBorehole(Action):

    async def execute(self, id, with_lock = True, user=None):

        permission = ''

        if user is not None:
            permission = """
                AND {}
            """.format(
                self.filterPermission(user)
            )

        sql_lock = ""
        if with_lock is True:
            sql_lock = f"""
                CASE
                    WHEN (
                        borehole.locked_by is NULL
                        OR (
                            borehole.locked_at < NOW()
                                - INTERVAL '{self.lock_timeout} minutes'
                        )
                    ) THEN NULL
                    ELSE (
                        select row_to_json(t2)
                        FROM (
                            SELECT
                                borehole.locked_by as id,
                                locker.username as username,
                                locker.firstname || ' ' || locker.lastname
                                    as fullname,
                                to_char(
                                    borehole.locked_at,
                                    'YYYY-MM-DD"T"HH24:MI:SS'
                                ) as date
                        ) t2
                    )
                END AS lock,
            """

        val = await self.conn.fetchval(f"""
            SELECT
                row_to_json(t)
            FROM (
                SELECT
                    borehole.id_bho as id,
                    borehole.public_bho as visible,
                    (
                        SELECT row_to_json(t)
                        FROM (
                            SELECT
                                updater.id_usr as id,
                                updater.username as username,
                                updater.firstname || ' ' || updater.lastname
                                    as fullname,
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
                    {sql_lock}
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
                        SELECT row_to_json(t)
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
                        SELECT row_to_json(t)
                        FROM (
                            SELECT
                                COALESCE(
                                    project_name_bho, ''
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
                                lithology_id_cli as lit_pet_top_bedrock,
                                lithostrat_id_cli as lit_str_top_bedrock,
                                chronostrat_id_cli AS chro_str_top_bedrock,
                                processing_status_id_cli
                                    as processing_status,
                                national_relevance_id_cli
                                    as national_relevance,
                                COALESCE(
                                    ate, '{{}}'::int[]
                                ) AS attributes_to_edit,
                                mistakes_bho as mistakes,
                                remarks_bho as remarks
                        ) t
                    ) as custom,
                    stratigraphy as stratigraphy,
                    completness.percentage,
                    (
                        SELECT row_to_json(t)
                        FROM (
                            SELECT
                                id_wgp as id,
                                name_wgp as name
                        ) t
                    ) as workgroup,
                    status[array_length(status, 1)] as workflow,
                    status[array_length(status, 1)]  ->> 'role' as "role"

                FROM
                    bdms.borehole

                INNER JOIN bdms.workgroups
                ON id_wgp = id_wgp_fk

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

                INNER JOIN bdms.completness
                    ON completness.id_bho = borehole.id_bho

                INNER JOIN bdms.users as updater
                    ON updater_bho = updater.id_usr

                INNER JOIN bdms.users as author
                    ON author_id = author.id_usr

                LEFT JOIN bdms.users as locker
                    ON locked_by = locker.id_usr

                LEFT JOIN bdms.cantons
                    ON kantonsnum = canton_bho

                LEFT JOIN bdms.municipalities
                    ON municipalities.gid = city_bho

                LEFT JOIN (
                    SELECT
                        id_bho_fk, array_agg(id_cli_fk) as ate
                    FROM
                        bdms.borehole_codelist
                    WHERE
                        code_cli = 'madm404'
                    GROUP BY id_bho_fk
                ) tmadm404
                    ON tmadm404.id_bho_fk = borehole.id_bho

                LEFT JOIN (
                    SELECT
                        id_bho_fk,
                        array_to_json(
                            array_agg(
                                json_build_object(
                                    'id', id,
                                    'kind', kind,
                                    'name', "name",
                                    'primary', "primary",
                                    'layers', layers,
                                    'date', date
                                )
                            )
                        ) AS stratigraphy
                    FROM (
                        SELECT
                            id_bho_fk,
                            id_sty AS id,
                            id_cli AS kind,
                            name_sty AS "name",
                            primary_sty as "primary",
                            to_char(
                                date_sty, 'YYYY-MM-DD'
                            ) AS date,
                            COUNT(id_lay) AS layers
                        FROM
                            bdms.stratigraphy
                        INNER JOIN bdms.codelist
                            ON kind_id_cli = id_cli
                        LEFT JOIN bdms.layer
                            ON id_sty_fk = id_sty
                        GROUP BY id_bho_fk, id_sty, id_cli, date_sty
                        ORDER BY date_sty DESC, id_sty DESC
                    ) t
                    GROUP BY id_bho_fk
                ) AS strt
                    ON strt.id_bho_fk = borehole.id_bho

                WHERE borehole.id_bho = $1
                {permission}
            ) AS t
        """, id)

        return {
            "data": self.decode(val) if val is not None else None
        }
