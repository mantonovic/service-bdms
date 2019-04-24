# -*- coding: utf-8 -*-
from bms.v1.action import Action
import math
from io import StringIO
import traceback
import csv


class ExportCsv(Action):

    async def execute(self, filter={}):

        where, params = self.filterBorehole(filter)

        sql = """
            SELECT
                id_bho as id,
                original_name_bho as original_name,
                knd.code_cli as kind,
                location_x_bho as location_x,
                location_y_bho as location_y,
                srd.code_cli as srs,
                elevation_z_bho as elevation_z,
                hrs.code_cli  as hrs,
                to_char(
                    drilling_date_bho,
                    'YYYY-MM-DD'
                ) as drilling_date,
                length_bho as length,
                rest.code_cli as restriction,
                to_char(
                    restriction_until_bho,
                    'YYYY-MM-DD'
                ) as restriction_until,
                meth.code_cli as method,
                prp.code_cli as purpose,
                sts.code_cli as status,
                top_bedrock_bho as top_bedrock,
                groundwater_bho as groundwater
            FROM
                borehole
            LEFT JOIN codelist as knd
                ON knd.id_cli = kind_id_cli
            LEFT JOIN codelist as srd
                ON srd.id_cli = srs_id_cli
            LEFT JOIN codelist as hrs
                ON hrs.id_cli = hrs_id_cli
            LEFT JOIN codelist as rest
                ON rest.id_cli = restriction_id_cli
            LEFT JOIN codelist as meth
                ON meth.id_cli = method_id_cli
            LEFT JOIN codelist as prp
                ON prp.id_cli = purpose_id_cli
            LEFT JOIN codelist as sts
                ON sts.id_cli = status_id_cli
        """

        if len(where) > 0:
            sql += """
                WHERE %s
            """ % " AND ".join(where)

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

        csvfile = StringIO()

        if len(data) > 0:
            cw = csv.writer(
                csvfile,
                delimiter=';',
                quotechar='"'
            )
            cols = data[0].keys()
            cw.writerow(cols)

            for row in data:
                r = []
                for col in cols:
                    r.append(row[col])
                cw.writerow(r)

        return csvfile
