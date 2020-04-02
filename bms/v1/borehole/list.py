# -*- coding: utf-8 -*-
from bms.v1.action import Action
import math


class ListBorehole(Action):

    def __init__(self, conn=None, geolcode=False):
        super(ListBorehole, self).__init__(conn=conn)
        self.geolcode = geolcode
    
    @staticmethod
    def get_sql_text(language='en', cols = None):
        fallback = 'en'
        return f"""
            SELECT
                id_bho as id,

                original_name_bho as original_name,
                project_name_bho as project_name,
                public_name_bho as public_name,
                COALESCE(
                    knd.text_cli_{language},
                    knd.text_cli_{fallback}
                ) as kind,

                COALESCE(
                    rest.text_cli_{language},
                    rest.text_cli_{fallback}
                ) as restriction,
                to_char(
                    restriction_until_bho,
                    'YYYY-MM-DD'
                ) as restriction_until,

                location_x_bho as location_x,
                location_y_bho as location_y,
                COALESCE(
                    srd.text_cli_{language},
                    srd.text_cli_{fallback}
                ) as srs,
                
                COALESCE(
                    qtloc.text_cli_{language},
                    qtloc.text_cli_{fallback}
                ) as qt_location,
                elevation_z_bho as elevation_z,
                COALESCE(
                    hrs.text_cli_{language},
                    hrs.text_cli_{fallback}
                ) as hrs,
                COALESCE(
                    qth.text_cli_{language},
                    qth.text_cli_{fallback}
                ) as qt_elevation,

                COALESCE(
                    lnd.text_cli_{language},
                    lnd.text_cli_{fallback}
                ) as landuse,
                cnt.name as canton,
                municipalities.name as city,
                address_bho as address,

                COALESCE(
                    meth.text_cli_{language},
                    meth.text_cli_{fallback}
                ) as method,
                to_char(
                    drilling_date_bho,
                    'YYYY-MM-DD'
                ) as drilling_date,
                COALESCE(
                    cut.text_cli_{language},
                    cut.text_cli_{fallback}
                ) as cuttings,
                COALESCE(
                    prp.text_cli_{language},
                    prp.text_cli_{fallback}
                ) as purpose,
                drill_diameter_bho as drill_diameter,
                COALESCE(
                    sts.text_cli_{language},
                    sts.text_cli_{fallback}
                ) as status,
                bore_inc_bho as bore_inc,
                bore_inc_dir_bho as bore_inc_dir,
                COALESCE(
                    qt_inc_dir.text_cli_{language},
                    qt_inc_dir.text_cli_{fallback}
                ) as qt_bore_inc_dir,

                length_bho as length,
                COALESCE(
                    qt_len.text_cli_{language},
                    qt_len.text_cli_{fallback}
                ) as qt_length,

                top_bedrock_bho as top_bedrock,

                COALESCE(
                    qt_tbed.text_cli_{language},
                    qt_tbed.text_cli_{fallback}
                ) as qt_top_bedrock,
                groundwater_bho as groundwater

                {f'{cols}' if cols else ''}

            FROM
                bdms.borehole

            LEFT JOIN bdms.codelist as qt_tbed
                ON qt_tbed.id_cli = qt_top_bedrock_id_cli

            LEFT JOIN bdms.codelist as rest
                ON rest.id_cli = restriction_id_cli

            LEFT JOIN bdms.codelist as knd
                ON knd.id_cli = kind_id_cli

            LEFT JOIN bdms.codelist as srd
                ON srd.id_cli = srs_id_cli

            LEFT JOIN bdms.codelist as qtloc
                ON qtloc.id_cli = qt_location_id_cli

            LEFT JOIN bdms.codelist as hrs
                ON hrs.id_cli = hrs_id_cli

            LEFT JOIN bdms.codelist as qth
                ON qth.id_cli = qt_elevation_id_cli

            LEFT JOIN bdms.codelist as lnd
                ON lnd.id_cli = landuse_id_cli

            LEFT JOIN (
                SELECT DISTINCT
                    cantons.kantonsnum,
                    cantons.name
                FROM
                    bdms.cantons
            ) AS cnt
            ON cnt.kantonsnum = canton_bho

            LEFT JOIN bdms.codelist as qt_len
                ON qt_len.id_cli = qt_length_id_cli

            LEFT JOIN bdms.codelist as qt_inc_dir
                ON qt_inc_dir.id_cli = qt_bore_inc_dir_id_cli

            LEFT JOIN bdms.codelist as cut
                ON cut.id_cli = cuttings_id_cli

            LEFT JOIN bdms.municipalities
                ON municipalities.gid = city_bho

            LEFT JOIN bdms.codelist as meth
                ON meth.id_cli = method_id_cli

            LEFT JOIN bdms.codelist as prp
                ON prp.id_cli = purpose_id_cli

            LEFT JOIN bdms.codelist as sts
                ON sts.id_cli = status_id_cli
        """

    @staticmethod
    def get_sql_geolcode(cols=None, join=None, where=None):
        return f"""
            SELECT
                id_bho as id,

                original_name_bho as original_name,
                project_name_bho as project_name,
                public_name_bho as public_name,
                knd.geolcode as kind,

                rest.geolcode as restriction,
                to_char(
                    restriction_until_bho,
                    'YYYY-MM-DD'
                ) as restriction_until,

                location_x_bho as location_x,
                location_y_bho as location_y,
                srd.geolcode as srs,
                
                qtloc.geolcode as qt_location,
                elevation_z_bho as elevation_z,
                hrs.geolcode as hrs,
                qth.geolcode as qt_elevation,

                lnd.geolcode as landuse,
                cnt.name as canton,
                municipalities.name as city,
                address_bho as address,

                meth.geolcode as method,
                to_char(
                    drilling_date_bho,
                    'YYYY-MM-DD'
                ) as drilling_date,
                cut.geolcode as cuttings,
                prp.geolcode as purpose,
                drill_diameter_bho as drill_diameter,
                sts.geolcode as status,
                bore_inc_bho as bore_inc,
                bore_inc_dir_bho as bore_inc_dir,
                qt_inc_dir.geolcode as qt_bore_inc_dir,

                length_bho as length,
                qt_len.geolcode as qt_length,

                top_bedrock_bho as top_bedrock,

                qt_tbed.geolcode as qt_top_bedrock,
                groundwater_bho as groundwater

                {f'{cols}' if cols else ''}

            FROM
                bdms.borehole

            LEFT JOIN (
                SELECT
                    id_bho_fk,
                    array_agg(id_cli_fk) as identifiers,
                    array_agg(value_bco) as identifiers_value
                FROM
                    bdms.borehole_codelist
                WHERE
                    code_cli = 'borehole_identifier'
                    GROUP BY id_bho_fk
            ) as ids
            ON
                ids.id_bho_fk = id_bho

            LEFT JOIN bdms.codelist as qt_tbed
                ON qt_tbed.id_cli = qt_top_bedrock_id_cli

            LEFT JOIN bdms.codelist as rest
                ON rest.id_cli = restriction_id_cli

            LEFT JOIN bdms.codelist as knd
                ON knd.id_cli = kind_id_cli

            LEFT JOIN bdms.codelist as srd
                ON srd.id_cli = srs_id_cli

            LEFT JOIN bdms.codelist as qtloc
                ON qtloc.id_cli = qt_location_id_cli

            LEFT JOIN bdms.codelist as hrs
                ON hrs.id_cli = hrs_id_cli

            LEFT JOIN bdms.codelist as qth
                ON qth.id_cli = qt_elevation_id_cli

            LEFT JOIN bdms.codelist as lnd
                ON lnd.id_cli = landuse_id_cli

            LEFT JOIN (
                SELECT DISTINCT
                    cantons.kantonsnum,
                    cantons.name
                FROM
                    bdms.cantons
            ) AS cnt
            ON cnt.kantonsnum = canton_bho

            LEFT JOIN bdms.codelist as qt_len
                ON qt_len.id_cli = qt_length_id_cli

            LEFT JOIN bdms.codelist as qt_inc_dir
                ON qt_inc_dir.id_cli = qt_bore_inc_dir_id_cli

            LEFT JOIN bdms.codelist as cut
                ON cut.id_cli = cuttings_id_cli

            LEFT JOIN bdms.municipalities
                ON municipalities.gid = city_bho

            LEFT JOIN bdms.codelist as meth
                ON meth.id_cli = method_id_cli

            LEFT JOIN bdms.codelist as prp
                ON prp.id_cli = purpose_id_cli

            LEFT JOIN bdms.codelist as sts
                ON sts.id_cli = status_id_cli

            {f'{join}' if join else ''}

            {f'{where}' if where else ''}
        """

    @staticmethod
    def get_sql():
        return """
            SELECT
                id_bho as id,
                (
                    select row_to_json(t)
                    FROM (
                        SELECT
                            author.id_usr as id,
                            author.username as username,
                            to_char(
                                created_bho,
                                'YYYY-MM-DD"T"HH24:MI:SSOF'
                            ) as date
                    ) t
                ) as author,
                original_name_bho as original_name,
                kind_id_cli as kind,
                restriction_id_cli as restriction,
                to_char(
                    restriction_until_bho,
                    'YYYY-MM-DD'
                ) as restriction_until,
                location_x_bho as location_x,
                location_y_bho as location_y,
                srs_id_cli as srs,
                elevation_z_bho as elevation_z,
                hrs_id_cli as hrs,
                drilling_date_bho as drilling_date,
                length_bho as length,
                (
                    select row_to_json(t)
                    FROM (
                        SELECT
                            status_id_cli as status,
                            purpose_id_cli as purpose,
                            top_bedrock_bho as top_bedrock
                    ) t
                ) as extended,
                status[array_length(status, 1)] as workflow,
                status[array_length(status, 1)]  ->> 'role' as "role"
            FROM
                bdms.borehole

            INNER JOIN
                bdms.users as author
            ON
                author_id = author.id_usr

            LEFT JOIN (
                SELECT
                    id_bho_fk,
                    array_agg(id_cli_fk) as borehole_identifier,
                    array_agg(value_bco) as identifier_value
                FROM
                    bdms.borehole_codelist
                WHERE
                    code_cli = 'borehole_identifier'
                    GROUP BY id_bho_fk
            ) as ids
            ON
                ids.id_bho_fk = id_bho

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
        """


    async def execute(
            self, limit=None, page=None,
            filter={}, orderby=None, direction=None, user=None
        ):

        permissions = None
        if user is not None:
            permissions = self.filterPermission(user)

        paging = ''

        where, params = self.filterBorehole(filter)

        if limit is not None and page is not None:
            paging = """
                LIMIT %s
                OFFSET %s
            """ % (self.getIdx(), self.getIdx())
            params += [
                limit, (int(limit) * (int(page) - 1))
            ]

        rowsSql = (
            self.get_sql_geolcode()
            if self.geolcode
            else self.get_sql()
        )

        cntSql = """
            SELECT
                count(*) AS cnt
            FROM
                bdms.borehole

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

            LEFT JOIN (
                SELECT
                    id_bho_fk,
                    array_agg(id_cli_fk) as borehole_identifier,
                    array_agg(value_bco) as identifier_value
                FROM
                    bdms.borehole_codelist
                WHERE
                    code_cli = 'borehole_identifier'
                    GROUP BY id_bho_fk
            ) as ids
            ON
                ids.id_bho_fk = id_bho
        """

        if len(where) > 0:
            rowsSql += """
                WHERE {}
            """.format(
                " AND ".join(where)
            )
            cntSql += """
                WHERE {}
            """.format(
                " AND ".join(where)
            )

        if permissions is not None:
            operator = 'AND' if len(where) > 0 else 'WHERE'
            rowsSql += """
                {} {}
            """.format(
                operator, permissions
            )
            cntSql += """
                {} {}
            """.format(
                operator, permissions
            )

        _orderby, direction = self.getordering(orderby, direction)

        sql = """
            SELECT
                array_to_json(
                    array_agg(
                        row_to_json(t)
                    )
                ),
                COALESCE((
                    %s
                ), 0)
            FROM (
                %s
            ORDER BY %s %s NULLS LAST
                %s
            ) AS t
        """ % (
            cntSql,
            rowsSql,
            _orderby,
            direction,
            paging
        )

        rec = await self.conn.fetchrow(
            sql, *(params)
        )
        return {
            "data": self.decode(rec[0]) if rec[0] is not None else [],
            "orderby": orderby,
            "direction": direction,
            "page": page if page is not None else 1,
            "pages": math.ceil(rec[1]/limit) if limit is not None else 1,
            "rows": rec[1]
        }
