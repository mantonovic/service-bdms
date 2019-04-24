# -*- coding: utf-8 -*-

from reportlab.lib.units import mm, cm
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import Spacer
from .pdfBase import PdfBase
import gettext
_ = gettext.gettext


class PdfBorehole(PdfBase):
    """docstring for OrdersExecutionPdf."""
    def __init__(self, debug=False):
        super(PdfBorehole, self).__init__(debug)
        self.data = None

    def prepare_pdf(self):
        self.prepare_header(self.data)

    def first_page(self, canvas, doc):
        canvas.saveState()
        canvas.drawInlineImage(
            'bms/assets/ch.png',
            self.doc.leftMargin,
            self.height - (19 + 1 * cm),
            width=24,
            height=24)

        if self.doc.title is not None:
            canvas.setFont('OpenSans', 8)
            canvas.drawCentredString(self.width / 2.0, 1 * cm, self.doc.title)

        textobject = canvas.beginText()
        textobject.setTextOrigin(
            self.doc.leftMargin + 1.2 * cm,
            self.height - 1.2 * cm
        )
        textobject.setFont('OpenSans', 10)
        textobject.setFillGray(0.4)
        textobject.textLine(_("Borehole Management System"))
        canvas.drawText(textobject)

        canvas.restoreState()

    def prepare_header(self, data):

        self.doc.title = datetime.now().strftime("%d.%m.%Y alle %H:%M")

        # self.add_paragraph(
        #     _("Location"),
        #     styles=self.paragraph_styles['title']
        # )

        colWidths = [
            ((self.get_innert_width()) * 25 / 100),
            ((self.get_innert_width()) * 25 / 100),
            ((self.get_innert_width()) * 25 / 100),
            ((self.get_innert_width()) * 25 / 100)
            # ((self.get_innert_width()) * 50 / 100)
        ]

        self.add_table(
            [
                [
                    self.create_paragraph(
                        _("Original name"),
                        self.paragraph_styles['label_left']),
                    self.create_paragraph(
                        _("Public name"),
                        self.paragraph_styles['label_left']),
                    self.create_paragraph(
                        _("Project name"),
                        self.paragraph_styles['label_left'])
                ],
                [
                    self.create_paragraph(
                        "foo",
                        self.paragraph_styles['content_big']),
                    self.create_paragraph(
                        "bar",
                        self.paragraph_styles['content_big']),
                    self.create_paragraph(
                        "foo",
                        self.paragraph_styles['content_big'])
                ],
                [
                    self.create_paragraph(
                        _("Drilling type"),
                        self.paragraph_styles['label_left']),
                    self.create_paragraph(
                        "",
                        self.paragraph_styles['label_left']),
                    self.create_paragraph(
                        _("Restriction"),
                        self.paragraph_styles['label_left']),
                    self.create_paragraph(
                        _("Restriction date"),
                        self.paragraph_styles['label_left'])
                ],
                [
                    self.create_paragraph(
                        "foo",
                        self.paragraph_styles['content']),
                    self.create_paragraph(
                        "bar",
                        self.paragraph_styles['content']),
                    self.create_paragraph(
                        "foo",
                        self.paragraph_styles['content']),
                    self.create_paragraph(
                        "bar",
                        self.paragraph_styles['content'])
                ]
            ],
            colWidths=colWidths,
            rowHeights=[None, 1 * cm, None, None],
            styles=[
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # ('VALIGN', (1, 0), (3, -1), 'TOP'),
                # ('VALIGN', (0, 0), (-1, -1), 'TOP')
                ('SPAN', (2, 0), (-1, 0)),
                ('SPAN', (2, 1), (-1, 1)),
                ('SPAN', (0, 2), (1, 2)),
                ('SPAN', (0, 3), (1, 3)),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]
        )

        self.add_paragraph(
            _("Coordinates"),
            styles=self.paragraph_styles['title']
        )

        self.add_table(
            [
                [
                    self.create_paragraph(
                        _("Coordinate East"),
                        self.paragraph_styles['label_left']),
                    self.create_paragraph(
                        _("Coordinate North"),
                        self.paragraph_styles['label_left']),
                    self.create_paragraph(
                        _("SRS"),
                        self.paragraph_styles['label_left']),
                    self.create_paragraph(
                        _("CQ Coordinates"),
                        self.paragraph_styles['label_left'])
                ],
                [
                    self.create_paragraph(
                        '<a href="https://map.geo.admin.ch/?lang=en&E=2708942&N=1114184&zoom=10&crosshair=marker" color="blue">click</a>',
                        self.paragraph_styles['content']),
                    self.create_paragraph(
                        "bar",
                        self.paragraph_styles['content']),
                    self.create_paragraph(
                        "foo",
                        self.paragraph_styles['content'])
                ],
                [
                    self.create_paragraph(
                        _("Elevation (masl)"),
                        self.paragraph_styles['label_left']),
                    self.create_paragraph(
                        _("HRS"),
                        self.paragraph_styles['label_left']),
                    self.create_paragraph(
                        _("CQ Elevation Z"),
                        self.paragraph_styles['label_left'])
                ],
                [
                    self.create_paragraph(
                        "foo",
                        self.paragraph_styles['content']),
                    self.create_paragraph(
                        "bar",
                        self.paragraph_styles['content']),
                    self.create_paragraph(
                        "foo",
                        self.paragraph_styles['content'])
                ]
            ],
            colWidths=[
                ((self.get_innert_width()) * 25 / 100),
                ((self.get_innert_width()) * 25 / 100),
                ((self.get_innert_width()) * 25 / 100),
                ((self.get_innert_width()) * 25 / 100)
            ],
            styles=[
                # ('VALIGN', (0, 0), (3, -1), 'BOTTOM'),
                # ('VALIGN', (1, 0), (3, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]
        )

        self.add_paragraph(
            _("Location"),
            styles=self.paragraph_styles['title']
        )

        self.add_table(
            [
                [
                    self.create_paragraph(
                        _("Canton"),
                        self.paragraph_styles['label_left']),
                    self.create_paragraph(
                        _("City"),
                        self.paragraph_styles['label_left'])
                ],
                [
                    self.create_paragraph(
                        "foo",
                        self.paragraph_styles['content']),
                    self.create_paragraph(
                        "bar",
                        self.paragraph_styles['content'])
                ],
                [
                    self.create_paragraph(
                        _("Address"),
                        self.paragraph_styles['label_left']),
                    self.create_paragraph(
                        _("Land use"),
                        self.paragraph_styles['label_left'])
                ],
                [
                    self.create_paragraph(
                        "foo",
                        self.paragraph_styles['content']),
                    self.create_paragraph(
                        "bar",
                        self.paragraph_styles['content'])
                ]
            ],
            colWidths=[
                ((self.get_innert_width()) * 50 / 100),
                ((self.get_innert_width()) * 50 / 100)
            ],
            styles=[
                # ('VALIGN', (0, 0), (3, -1), 'BOTTOM'),
                # ('VALIGN', (1, 0), (3, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]
        )