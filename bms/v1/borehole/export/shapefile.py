# -*- coding: utf-8 -*-
from bms.v1.action import Action
import math
from io import BytesIO
import traceback
import shapefile


class ExportShapefile(Action):

    async def execute(self, filter={}, user=None):

        permissions = None
        if user is not None:
            permissions = self.filterPermission(user)

        where, params = self.filterBorehole(filter)
        sql = """
            SELECT
                id_bho as id,
                original_name_bho as original_name,
                knd.code_cli as kind,
                st_x(geom_bho) AS x,
                st_y(geom_bho) AS y
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

            LEFT JOIN bdms.codelist as knd
                ON knd.id_cli = kind_id_cli

            LEFT JOIN bdms.codelist as srd
                ON srd.id_cli = srs_id_cli

            LEFT JOIN bdms.codelist as hrs
                ON hrs.id_cli = hrs_id_cli

            LEFT JOIN bdms.codelist as rest
                ON rest.id_cli = restriction_id_cli

            LEFT JOIN bdms.codelist as meth
                ON meth.id_cli = method_id_cli

            LEFT JOIN bdms.codelist as prp
                ON prp.id_cli = purpose_id_cli

            LEFT JOIN bdms.codelist as sts
                ON sts.id_cli = status_id_cli

            WHERE geom_bho IS NOT NULL
        """

        if len(where) > 0:
            sql += """
                AND %s
            """ % " AND ".join(where)

        if permissions is not None:
            sql += f"""
                AND {permissions}
            """

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

            prj = BytesIO(
                b'PROJCS["CH1903+_LV95",GEOGCS["GCS_CH1903+",' \
                b'DATUM["D_CH1903+",SPHEROID["Bessel_1841",' \
                b'6377397.155,299.1528128]],PRIMEM["Greenwich",0],' \
                b'UNIT["Degree",0.017453292519943295]],PROJECTION' \
                b'["Hotine_Oblique_Mercator_Azimuth_Center"],PARAMETER' \
                b'["latitude_of_center",46.95240555555556],' \
                b'PARAMETER["longitude_of_center",7.439583333333333],' \
                b'PARAMETER["azimuth",90],PARAMETER["scale_factor",1],' \
                b'PARAMETER["false_easting",2600000],' \
                b'PARAMETER["false_northing",1200000],UNIT["Meter",1]]'
                
            )

        return shp, shx, dbf, prj
