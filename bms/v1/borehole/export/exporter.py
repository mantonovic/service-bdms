# -*- coding: utf-8 -*-S
from bms.v1.handlers import Viewer
from bms.v1.borehole.export.csv import ExportCsv
from bms.v1.borehole.export.shapefile import ExportShapefile
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

class ExportHandler(Viewer):
    async def get(self, *args, **kwargs):
        try:

            if self.user is None:
                raise AuthenticationException()

            self.authorize()

            arguments = {}
            for key in self.request.query_arguments.keys():
                print("key: '%s'" % key)
                if self.request.query_arguments[key][0] != b'null':
                    if key == 'extent':
                        coords = self.get_argument(key).split(',')
                        for idx in range(0, len(coords)):
                            coords[idx] = float(coords[idx])
                        arguments[key] = coords
                    else:                        
                        if key == 'format':
                            print(" > Splitting..")
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

                    action = ExportCsv(conn)
                    if arguments is None:
                        csvfile = await action.execute()
                    else:
                        csvfile = await action.execute(filter=arguments)

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

                    def append_pdf(input, output):
                        [
                            output.addPage(
                                input.getPage(page_num)
                            ) for page_num in range(input.numPages)
                        ]

                    # precedent_file = None
                    working_file = None

                    pdfs = []

                    pdf = PdfBorehole()
                    pdf.prepare_pdf()
                    pdf.save()

                    pdfs.append(pdf)

                    outputFW = PdfFileWriter()
                    for pdf in pdfs:
                        inpt = PdfFileReader(pdf.pdf)
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
                        shp, shx, dbf = await shpA.execute()
                    else:
                        shp, shx, dbf = await shpA.execute(filter=arguments)

                    print("Done..")

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

    # async def post(self, *args, **kwargs):
    #     try:
    #         self.set_header("Content-Type", "text/csv")
    #         if self.user is None:
    #             raise AuthenticationException()

    #         self.authorize()
    #         body = self.request.body.decode('utf-8')
    #         if body is None or body == '':
    #             raise ActionEmpty()

    #         async with self.pool.acquire() as conn:
    #             action = ExportBorehole(conn)
    #             result = await action.execute(**json.loads(body))
    #             data = result['data']
    #             if len(data) > 0:
    #                 csvfile = StringIO()
    #                 cw = csv.writer(
    #                     csvfile,
    #                     delimiter=';',
    #                     quotechar='"'
    #                 )
    #                 cols = data[0].keys()
    #                 cw.writerow(cols)

    #                 for row in data:
    #                     r = []
    #                     for col in cols:
    #                         r.append(row[col])
    #                     cw.writerow(r)

    #                 self.write(csvfile.getvalue())

    #             else:
    #                 self.write("no data")

    #     except BmsException as bex:
    #         print(traceback.print_exc())
    #         self.write({
    #             "success": False,
    #             "message": str(bex),
    #             "error": bex.code
    #         })
    #     except Exception as ex:
    #         print(traceback.print_exc())
    #         self.write({
    #             "success": False,
    #             "message": str(ex)
    #         })
    #     self.finish()
