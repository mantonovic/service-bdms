# -*- coding: utf-8 -*-
from bms.v1.action import Action
import math
from io import BytesIO
import traceback
import shapefile


class ExportShapefile(Action):

    async def execute(self, filter={}):

        where, params = self.filterBorehole(filter)
        sql = """
            SELECT
                id_bho as id,
                original_name_bho as original_name,
                knd.code_cli as kind,
                st_x(geom_bho) AS x,
                st_y(geom_bho) AS y
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
            WHERE geom_bho IS NOT NULL
        """

        if len(where) > 0:
            sql += """
                WHERE %s
            """ % " AND ".join(where)

        recs = await self.conn.fetch(sql, *(params))

        if len(recs) > 0:

            shp = BytesIO()
            shx = BytesIO()
            dbf = BytesIO()

            w = shapefile.Writer(
                shp=shp, shx=shx, dbf=dbf
            )

            w.field('NAME', 'C')
            w.field('KIND', 'C')
            # w.field('DATE', 'D')

            for rec in recs:
                w.point(rec[3], rec[4]) 
                w.record(rec[1], rec[2])

            w.close()

        return shp, shx, dbf
