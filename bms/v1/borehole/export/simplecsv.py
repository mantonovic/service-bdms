# -*- coding: utf-8 -*-
from bms.v1.action import Action
from bms.v1.borehole.codelist import ListCodeList
import math
from io import StringIO
import traceback
import csv


class ExportSimpleCsv(Action):

    async def execute(self, filter={}, user=None):

        language = 'en'
        if (
            'language' in filter
            and filter['language'] in ['it', 'de', 'fr']
        ):
            language = filter['language']

        permissions = None
        if user is not None:
            permissions = self.filterPermission(user)

        where, params = self.filterBorehole(filter)

        sql = """
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

        if len(where) > 0:
            sql += """
                WHERE %s
            """ % " AND ".join(where)

        if permissions is not None:
            operator = 'AND' if len(where) > 0 else 'WHERE'
            sql += f"""
                {operator} {permissions}
            """

        rec = await self.conn.fetchval(
            """
            SELECT
                array_to_json(
                    array_agg(
                        row_to_json(t)
                    )
                )
            FROM (
                %s
                ORDER BY 1
            ) AS t
        """ % sql, *(params))

        data = self.decode(rec) if rec is not None else []

        cl = await ListCodeList(self.conn).execute('borehole_form')

        csv_header = {}
        for c in cl['data']['borehole_form']:
            csv_header[c['code']] = c

        csvfile = StringIO()

        if len(data) > 0:
            cw = csv.writer(
                csvfile,
                delimiter=';',
                quotechar='"'
            )
            # cols = data[0].keys()
            keys = data[0].keys()
            cols = []
            for key in keys:
                cols.append(
                    csv_header[key][language]['text']
                    if key in csv_header else key
                )

            cw.writerow(cols)

            for row in data:
                r = []
                for col in keys:
                    if isinstance(row[col], list):
                        r.append(",".join(str(x) for x in row[col]))
                    else:
                        r.append(row[col])
                cw.writerow(r)

        return csvfile
