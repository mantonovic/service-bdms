# -*- coding: utf-8 -*-
from bms.v1.handlers import Viewer
from bms.v1.borehole.export import (
    ExportSimpleCsv,
    ExportShapefile,
    ExportCsv
)
from .pdf import PdfBorehole
from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO
import zipfile
import traceback
from bms.v1.exceptions import (
    BmsException,
    AuthenticationException,
    ActionEmpty,
    MissingParameter
)
import json
import datetime
from .profile import bdms_pdf as bdms


class ExportHandler(Viewer):
    async def get(self, *args, **kwargs):
        try:

            if self.user is None:
                raise AuthenticationException()

            self.authorize()

            arguments = {}
            for key in self.request.query_arguments.keys():
                if self.request.query_arguments[key][0] != b'null':
                    if key == 'extent':
                        coords = self.get_argument(key).split(',')
                        for idx in range(0, len(coords)):
                            coords[idx] = float(coords[idx])
                        arguments[key] = coords
                    elif key == 'format':
                        arguments[key] = self.get_argument(key).split(',')
                    else:
                        arguments[key] = self.get_argument(key)

            if 'format' not in arguments.keys():
                raise MissingParameter("format")

            now = datetime.datetime.now()

            self.set_header(
                "Expires",
                datetime.datetime.utcnow() +
                datetime.timedelta(seconds=1)
            )

            self.set_header(
                "Cache-Control",
                "max-age=" + str(1)
            )

            async with self.pool.acquire() as conn:

                output = None
                output_stream = None

                if len(arguments['format']) > 1:

                    self.set_header(
                        "Content-Type",
                        "application/zip"
                    )
                    self.set_header(
                        "Content-Disposition",
                        "inline; filename=export-%s.zip" % now.strftime(
                                "%Y%m%d%H%M%S"
                        )
                    )

                    output = BytesIO()
                    output_stream = zipfile.ZipFile(
                        output,
                        mode="w",
                        compression=zipfile.ZIP_DEFLATED
                    )

                if 'csv' in arguments['format']:

                    # action = ExportSimpleCsv(conn)
                    action = ExportCsv(conn)
                    if arguments is None:
                        csvfile = await action.execute(
                            user=self.user
                        )

                    else:
                        csvfile = await action.execute(
                            filter=arguments,
                            user=self.user
                        )


                    if output_stream is not None:
                        output_stream.writestr(
                            'export-%s.csv' % now.strftime(
                                    "%Y%m%d%H%M%S"
                            ),
                            csvfile.getvalue()
                        )

                    else:
                        self.set_header(
                            "Content-Type",
                            "text/csv"
                        )
                        self.set_header(
                            "Content-Disposition",
                            "inline; filename=export-%s.csv" % now.strftime(
                                    "%Y%m%d%H%M%S"
                            )
                        )
                        self.write(csvfile.getvalue())

                if 'pdf' in arguments['format']:

                    lan = arguments['lang'] if 'lang' in arguments else 'en'
                    idsty =6
                    schema ='bdms'

                    if 'id' in arguments:

                        pdfs = []

                        for cid in arguments['id'].split(','):
                            cid = cid.split(':')
                            if len(cid)==2:
                                bid = int(cid[0])
                                sid = int(cid[1])

                                # TODO: test if passed sid belongs to passed bid
                                # else raise error
                            elif len(cid)==1:
                                bid = int(cid[0])
                                sid = await conn.fetchval("""
                                    SELECT
                                        id_sty
                                    FROM
                                        bdms.stratigraphy
                                    WHERE
                                        id_bho_fk = $1
                                    AND
                                        primary_sty IS TRUE
                                """, bid)
                                print("SID:",sid)
                            else:
                                raise ValueError("id parameters are {berehole id}:{stratigraphy id}")

                            print(f"Processing berehole id {bid} and stratigraphy id {sid}")

                            if sid is not None:
                                        
                                res = await conn.fetchval("""
                                    SELECT
                                        row_to_json(t2)
                                    FROM (
                                        SELECT
                                            id_bho as idb,
                                            'Switzerland' as country,
                                            cant_j.name as canton,
                                            mun_j.name as city,
                                            address_bho as address,
                                            cli_kind.text_cli_{} as kind,
                                            location_x_bho as location_e,
                                            location_y_bho as location_n,
                                            COALESCE(elevation_z_bho, 0) as elevation_z,
                                            cli_srs.text_cli_{} as srs,
                                            cli_hrs.text_cli_{} as hrs,
                                            length_bho as length,
                                            drilling_date_bho as drilling_date,
                                            cli_restriction.text_cli_{} as restriction,
                                            to_char(
                                                restriction_until_bho,
                                                'YYYY-MM-DD'
                                            ) as restrictoin_until,
                                            cli_purpose.text_cli_{} as purpose,
                                            cli_landuse.text_cli_{} as landuse,
                                            cli_cuttings.text_cli_{} as cuttings,
                                            cli_method.text_cli_{} as method,
                                            cli_status.text_cli_{} as status,
                                            drill_diameter_bho as drill_diameter,
                                            bore_inc_bho as bore_inc,
                                            bore_inc_dir_bho as bore_inc_dir,
                                            project_name_bho as project_name,
                                            '12345' as auth_n,
                                            original_name_bho as original_name,
                                            public_name_bho as public_name,
                                            strat_j.name_sty as strataname,
                                            strat_j.date_sty as stratadate,
                                            'IFEC' as logged_by,
                                            'swisstopo' as checked_by,
                                            groundwater_bho as groundwater,

                                            (SELECT
                                                array_to_json(
                                                    array_agg(
                                                        row_to_json(t)
                                                    )
                                                )
                                                FROM (
                                                    SELECT
                                                        id_lay as id,
                                                        id_sty as id_sty,
                                                        depth_from_lay as depth_from,
                                                        depth_to_lay as depth_to,
                                                        CASE
                                                            WHEN elevation_z_bho is NULL 
                                                            THEN 0 - depth_from_lay
                                                            ELSE elevation_z_bho - depth_from_lay
                                                        END AS msm_from,
                                                        CASE
                                                            WHEN elevation_z_bho is NULL 
                                                            THEN 0 - depth_to_lay
                                                            ELSE elevation_z_bho - depth_to_lay
                                                        END AS msm_to,
                                                        cli_lithostra.text_cli_{} as lithostratigraphy,
                                                        cli_lithostra.conf_cli as conf_lithostra,
                                                        cli_lithostra.geolcode as geolcode_lithostra,
                                                        cli_lithology.text_cli_{} as lithology,
                                                        cli_lithology.conf_cli as conf_lithology,
                                                        description_lay as layer_desc,
                                                        geology_lay as geol_desc,
                                                        name_sty as name_st,
                                                        notes_lay as notes
                                                    FROM
                                                        {}.layer
                                                            LEFT JOIN {}.codelist as cli_lithostra
                                                                ON cli_lithostra.id_cli = lithostratigraphy_id_cli
                                                            LEFT JOIN {}.codelist as cli_lithology
                                                                ON cli_lithology.id_cli = lithology_id_cli,
                                                        {}.stratigraphy,
                                                        {}.borehole
                                                    WHERE
                                                        id_sty_fk = id_sty
                                                    AND
                                                        id_sty = $1
                                                    AND
                                                        id_bho_fk = id_bho
                                                    AND
                                                        id_bho = strat_j.id_bho_fk
                                                    ORDER BY depth_from_lay, id_lay

                                            ) AS t
                                        ) AS layers 
                                        FROM 
                                            {}.borehole
                                        LEFT JOIN {}.codelist as cli_kind
                                            ON cli_kind.id_cli = kind_id_cli
                                        LEFT JOIN {}.codelist as cli_srs
                                            ON cli_srs.id_cli = srs_id_cli
                                        LEFT JOIN {}.codelist as cli_hrs
                                            ON cli_hrs.id_cli = hrs_id_cli
                                        LEFT JOIN {}.codelist as cli_restriction
                                            ON cli_restriction.id_cli = restriction_id_cli
                                        LEFT JOIN {}.codelist as cli_purpose
                                            ON cli_purpose.id_cli = purpose_id_cli
                                        LEFT JOIN {}.codelist as cli_method
                                            ON cli_method.id_cli = method_id_cli
                                        LEFT JOIN {}.codelist as cli_landuse
                                            ON cli_landuse.id_cli =landuse_id_cli
                                        LEFT JOIN {}.codelist as cli_status
                                            ON cli_status.id_cli =status_id_cli
                                        LEFT JOIN {}.codelist as cli_cuttings
                                            ON cli_cuttings.id_cli = cuttings_id_cli
                                        LEFT JOIN {}.municipalities as mun_j
                                            ON mun_j.gid = city_bho
                                        LEFT JOIN {}.cantons as cant_j
                                            ON cant_j.gid = canton_bho
                                        LEFT JOIN (
                                            SELECT id_sty, date_sty, name_sty, id_bho_fk 
                                            FROM {}.stratigraphy
                                            --WHERE primary_sty = true
                                        ) as strat_j ON strat_j.id_sty = $2
                                                
                                        WHERE
                                            id_bho = id_bho_fk
                                        AND
                                            strat_j.id_sty = $3
                                    ) AS t2
                                """.format(*((lan,)*11 + (schema,)*18)), sid, sid, sid)

                                print(res)

                                a = bdms.bdmsPdf( json.loads(res))
                                a.renderProfilePDF(
                                    arguments['lang'] if 'lang' in arguments else 'en',
                                    int(arguments['scale']) if 'scale' in arguments else 200
                                )
                                a.close()

                                pdfs.append(a.pdf)

                    def append_pdf(input, output):
                        [
                            output.addPage(
                                input.getPage(page_num)
                            ) for page_num in range(input.numPages)
                        ]

                    outputFW = PdfFileWriter()
                    for pdf in pdfs:
                        inpt = PdfFileReader(pdf)
                        if inpt.isEncrypted:
                            inpt.decrypt('')
                        append_pdf(inpt, outputFW)

                    working_file = BytesIO()
                    outputFW.write(working_file)

                    if output_stream is not None:
                        output_stream.writestr(
                            'export-%s.pdf' % now.strftime(
                                    "%Y%m%d%H%M%S"
                            ),
                            working_file.getvalue()
                        )

                    else:
                        self.set_header(
                            "Content-Type",
                            "application/pdf"
                        )
                        self.set_header(
                            "Content-Disposition",
                            "inline; filename=export-%s.pdf" % now.strftime(
                                    "%Y%m%d%H%M%S"
                            )
                        )
                        self.write(working_file.getvalue())

                if 'shape' in arguments['format']:

                    shpA = ExportShapefile(conn)

                    if arguments is None:
                        shp, shx, dbf, prj = await shpA.execute(
                            user=self.user
                        )
                    else:
                        shp, shx, dbf, prj = await shpA.execute(
                            filter=arguments,
                            user=self.user
                        )

                    if output_stream is None:
                        self.set_header(
                            "Content-Type",
                            "application/zip"
                        )
                        self.set_header(
                            "Content-Disposition",
                            "inline; filename=export-%s.zip" % now.strftime(
                                    "%Y%m%d%H%M%S"
                            )
                        )
                        output = BytesIO()
                        output_stream = zipfile.ZipFile(
                            output,
                            mode="w",
                            compression=zipfile.ZIP_DEFLATED
                        )

                    output_stream.writestr(
                        'export-%s.shp' % now.strftime(
                                "%Y%m%d%H%M%S"
                        ),
                        shp.getvalue()
                    )
                    output_stream.writestr(
                        'export-%s.shx' % now.strftime(
                                "%Y%m%d%H%M%S"
                        ),
                        shx.getvalue()
                    )
                    output_stream.writestr(
                        'export-%s.dbf' % now.strftime(
                                "%Y%m%d%H%M%S"
                        ),
                        dbf.getvalue()
                    )
                    output_stream.writestr(
                        'export-%s.prj' % now.strftime(
                                "%Y%m%d%H%M%S"
                        ),
                        prj.getvalue()
                    )

            if output_stream is not None:
                output_stream.close()
                self.write(output.getvalue())

        except BmsException as bex:
            print(traceback.print_exc())
            self.write({
                "success": False,
                "message": str(bex),
                "error": bex.code
            })
        except Exception as ex:
            print(traceback.print_exc())
            self.write({
                "success": False,
                "message": str(ex)
            })
        self.finish()
