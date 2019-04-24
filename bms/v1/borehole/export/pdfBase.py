# -*- coding: utf-8 -*-
"""
Created on 20161008

@author: milan antonovic
"""

# from tornado import gen

from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import landscape
# from reportlab.lib.units import mm
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    PageTemplate,
    NextPageTemplate,
    Frame
    # Image
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import (
    TA_LEFT,
    TA_CENTER,
    # TA_JUSTIFY,
    TA_RIGHT
)
from reportlab.lib.colors import (
    Color,
    black,
    purple,
    # white,
    yellow
)
from io import BytesIO


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        self.width, self.height = A4
        # self.setPageSize(landscape(A4))

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("OpenSans", 8)
        self.drawRightString(
            self.width - 1.5 * cm, 1 * cm,
            "%d/%d" % (self._pageNumber, page_count))


class NumberedCanvasLandscape(NumberedCanvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        self.width, self.height = landscape(A4)


def make_landscape(canvas, doc):
    canvas.setPageSize(landscape(A4))


class PdfBase(object):

    def __init__(self, debug=False, ls=False):
        # self.pdf = tempfile.NamedTemporaryFile()
        # self.doc = SimpleDocTemplate(self.pdf.name)
        self.pdf = BytesIO()
        if ls:
            self.ls = True
            self.doc = SimpleDocTemplate(
                self.pdf,
                pagesize=landscape(A4)
            )
            self.width, self.height = landscape(A4)
        else:
            self.ls = False
            self.doc = SimpleDocTemplate(
                self.pdf,
                pagesize=A4
            )
            self.width, self.height = A4

        self.doc.leftMargin = 1.5 * cm
        self.doc.rightMargin = 1 * cm
        self.debug = debug
        if debug:
            self.doc.showBoundary = 1
        self.story = []
        self.init_style_sheet()
        # self.styles = getSampleStyleSheet()
        # self.canvas = self.doc.canv
        # self.canvas = canvas.Canvas(self.pdf.name, pagesize=A4)

    # Used with "with" statement
    def __enter__(self):
        return self

    # Used with "with" statement
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.pdf:
            self.pdf.close()

    '''def __del__(self):
        if self.pdf:
            print "Destroying temp file: %s" % self.pdf.name
            self.pdf.close()'''

    def first_page(self, canvas, doc):
        canvas.saveState()
        canvas.setPageSize(landscape(A4))
        canvas.drawInlineImage(
            'assets/img/logo-header-pdf.jpg',
            self.width / 2, # - 55.5,
            self.height / 2, # - (19 + 1 * cm),
            width=111,
            height=24)
        if self.doc.title is not None:
            canvas.setFont('OpenSans', 8)
            canvas.drawCentredString(self.width / 2.0, 1 * cm, self.doc.title)
        canvas.restoreState()

    def add_paragraph(self, text, space=True, styles=None):
        self.story.append(self.create_paragraph(text, styles=styles))
        if space:
            self.story.append(Spacer(1, 0.3 * cm))

    def create_paragraph(self, text, styles=None):
        if styles is None:
            styles = self.paragraph_styles['default']
        return Paragraph(text, styles)

    def get_innert_width(self):
        return (
            self.width -
            self.doc.leftMargin -
            self.doc.rightMargin
        )

    def add_table(self, data, colWidths=None, styles=[], rowHeights=None):
        if colWidths is None:
            colWidths = self.get_innert_width() / len(data[0])
        if self.debug:
            styles.append(('GRID', (0, 0), (-1, -1), 0.5, colors.grey))
        self.story.append(
            Table(
                data,
                colWidths=colWidths,
                rowHeights=rowHeights,
                style=styles
            )
        )

    def save(self):
        # self.canvas.showPage()
        # self.canvas.save()
        self.doc.build(
            self.story,
            onFirstPage=self.first_page,
            onLaterPages=self.first_page,
            canvasmaker=NumberedCanvasLandscape if self.ls else NumberedCanvas)

    def set_properties(self, title, subject, author):
        self.doc.title = title
        self.doc.subject = subject
        self.doc.author = author
        # self.canvas.setTitle(title)
        # self.canvas.setSubject(subject)
        # self.canvas.setAuthor(author)

    def set_footer(self):
        pass

    def init_style_sheet(self):
        pdfmetrics.registerFont(
            TTFont('Roboto', 'bms/assets/font/Roboto/Roboto-Regular.ttf'))
        pdfmetrics.registerFont(
            TTFont('OpenSans-Bold', 'bms/assets/font/Open_Sans/OpenSans-Bold.ttf'))
        pdfmetrics.registerFont(
            TTFont('OpenSans', 'bms/assets/font/Open_Sans/OpenSans-Regular.ttf'))
        paragraph_border_color = None
        if self.debug:
            paragraph_border_color = black
        self.paragraph_styles = {
            'default': ParagraphStyle(
                'default',
                fontName='OpenSans',
                fontSize=10,
                leading=12,
                leftIndent=0,
                rightIndent=0,
                firstLineIndent=0,
                alignment=TA_LEFT,
                spaceBefore=0,
                spaceAfter=0,
                bulletFontName='OpenSans',
                bulletFontSize=10,
                bulletIndent=0,
                textColor=Color(0, 0, 0, 0.87),
                backColor=None,
                wordWrap=None,
                borderWidth=1,
                borderPadding=0,
                borderColor=paragraph_border_color,
                borderRadius=None,
                allowWidows=1,
                allowOrphans=0,
                textTransform=None,  # 'uppercase' | 'lowercase' | None
                endDots=None,
                splitLongWords=1
            )
        }
        self.paragraph_styles['label_right'] = ParagraphStyle(
            'label_right',
            parent=self.paragraph_styles['default'],
            alignment=TA_RIGHT,
            fontName='OpenSans',
            fontSize=8,
            textColor=Color(0.4, 0.4, 0.4, 1)
        )
        self.paragraph_styles['label_2'] = ParagraphStyle(
            'label_2',
            parent=self.paragraph_styles['label_right'],
            alignment=TA_RIGHT,
            fontName='OpenSans-Bold',
            textColor=Color(0.0, 0.0, 0.0, 1)
        )
        self.paragraph_styles['label_left'] = ParagraphStyle(
            'label_left',
            parent=self.paragraph_styles['label_right'],
            alignment=TA_LEFT
        )
        self.paragraph_styles['label_3_big'] = ParagraphStyle(
            'label_3_big',
            parent=self.paragraph_styles['label_left'],
            fontSize=14
        )
        self.paragraph_styles['content'] = ParagraphStyle(
            'content',
            fontName='OpenSans-Bold',
            parent=self.paragraph_styles['default']
        )
        self.paragraph_styles['content_big'] = ParagraphStyle(
            'content_big',
            parent=self.paragraph_styles['content'],
            fontSize=16
        )
        self.paragraph_styles['note_title'] = ParagraphStyle(
            'note_title',
            parent=self.paragraph_styles['default'],
            fontName='OpenSans-Bold',
            fontSize=11
        )
        self.paragraph_styles['title'] = ParagraphStyle(
            'title',
            parent=self.paragraph_styles['default'],
            fontName='OpenSans-Bold',
            fontSize=14,
            spaceBefore=10,
            leading=18,
            alignment=TA_LEFT
        )
        self.paragraph_styles['alert'] = ParagraphStyle(
            'alert',
            parent=self.paragraph_styles['default'],
            leading=14,
            backColor=yellow,
            borderColor=black,
            borderWidth=1,
            borderPadding=5,
            borderRadius=2,
            spaceBefore=10,
            spaceAfter=10
        )
