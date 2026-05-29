"""
QR Code Tools Management System — User Guide PDF Generator
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import os

OUTPUT_PATH = "E:/QR/public/QR_Tools_Management_UserGuide.pdf"

# ── Colour Palette ──────────────────────────────────────────────────────────
PRIMARY      = HexColor("#1E3A5F")   # dark navy
ACCENT       = HexColor("#2E86DE")   # bright blue
SUCCESS      = HexColor("#27AE60")   # green
WARNING_COL  = HexColor("#F39C12")   # amber
DANGER       = HexColor("#E74C3C")   # red
INFO_COL     = HexColor("#3498DB")   # sky blue
LIGHT_BG     = HexColor("#F0F4F8")   # very light blue-grey
MID_BG       = HexColor("#D6E4F0")   # medium blue-grey
TABLE_HEADER = HexColor("#1E3A5F")
TABLE_ALT    = HexColor("#EBF5FB")
FLOW_BG      = HexColor("#FAFBFC")
FLOW_BORDER  = HexColor("#BDC3C7")
WHITE        = colors.white
BLACK        = colors.black

W, H = A4


# ── Custom Flowables ─────────────────────────────────────────────────────────

class FlowBox(Flowable):
    """A styled box for user-flow steps."""
    def __init__(self, lines, width=None, bg=FLOW_BG, border=FLOW_BORDER):
        super().__init__()
        self._lines = lines
        self._width = width or (W - 2 * 2.0 * cm)
        self._bg = bg
        self._border = border
        # estimate height: 14pt per line + 16pt padding
        self.height = len(lines) * 14 + 20

    def wrap(self, availW, availH):
        self._width = availW
        return self._width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        # background
        c.setFillColor(self._bg)
        c.roundRect(0, 0, self._width, self.height, 6, fill=1, stroke=0)
        # border
        c.setStrokeColor(self._border)
        c.setLineWidth(0.8)
        c.roundRect(0, 0, self._width, self.height, 6, fill=0, stroke=1)
        # left accent bar
        c.setFillColor(ACCENT)
        c.rect(0, 0, 4, self.height, fill=1, stroke=0)
        # text
        c.setFillColor(PRIMARY)
        c.setFont("Courier", 8.5)
        y = self.height - 12
        for line in self._lines:
            c.drawString(14, y, line)
            y -= 13
        c.restoreState()


class SectionBanner(Flowable):
    """Full-width coloured banner for section headings."""
    def __init__(self, text, number=None, width=None):
        super().__init__()
        self._text = text
        self._number = number
        self._width = width or (W - 2 * 2.0 * cm)
        self.height = 28

    def wrap(self, availW, availH):
        self._width = availW
        return self._width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        # gradient-like: solid primary then lighter strip
        c.setFillColor(PRIMARY)
        c.roundRect(0, 0, self._width, self.height, 5, fill=1, stroke=0)
        c.setFillColor(ACCENT)
        c.roundRect(self._width - 8, 0, 8, self.height, 0, fill=1, stroke=0)
        # number badge
        if self._number:
            c.setFillColor(ACCENT)
            c.circle(18, self.height / 2, 9, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(18, self.height / 2 - 3, str(self._number))
        # section text
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 12)
        x_start = 36 if self._number else 14
        c.drawString(x_start, self.height / 2 - 4, self._text)
        c.restoreState()


class SubHeading(Flowable):
    """Coloured sub-section bar."""
    def __init__(self, text, width=None):
        super().__init__()
        self._text = text
        self._width = width or (W - 2 * 2.0 * cm)
        self.height = 20

    def wrap(self, availW, availH):
        self._width = availW
        return self._width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(MID_BG)
        c.roundRect(0, 0, self._width, self.height, 4, fill=1, stroke=0)
        c.setFillColor(ACCENT)
        c.rect(0, 0, 4, self.height, fill=1, stroke=0)
        c.setFillColor(PRIMARY)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(12, 5, self._text)
        c.restoreState()


class AlertBox(Flowable):
    """Coloured alert/callout box."""
    COLOURS = {
        "critical": DANGER,
        "warning":  WARNING_COL,
        "info":     INFO_COL,
        "success":  SUCCESS,
        "note":     ACCENT,
    }

    def __init__(self, label, text, kind="note", width=None):
        super().__init__()
        self._label = label
        self._text  = text
        self._kind  = kind
        self._width = width or (W - 2 * 2.0 * cm)
        self.height = 30

    def wrap(self, availW, availH):
        self._width = availW
        return self._width, self.height

    def draw(self):
        c = self.canv
        col = self.COLOURS.get(self._kind, ACCENT)
        c.saveState()
        c.setFillColor(col)
        c.setFillAlpha(0.12)
        c.roundRect(0, 0, self._width, self.height, 5, fill=1, stroke=0)
        c.setFillAlpha(1)
        c.setStrokeColor(col)
        c.setLineWidth(1.2)
        c.roundRect(0, 0, self._width, self.height, 5, fill=0, stroke=1)
        c.setFillColor(col)
        c.rect(0, 0, 5, self.height, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(12, self.height - 14, self._label)
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 9)
        c.drawString(12, 8, self._text)
        c.restoreState()


# ── Page Template ─────────────────────────────────────────────────────────────

def make_header_footer(canvas_obj, doc):
    canvas_obj.saveState()
    W_p, H_p = A4
    # Header bar
    canvas_obj.setFillColor(PRIMARY)
    canvas_obj.rect(0, H_p - 22*mm, W_p, 12*mm, fill=1, stroke=0)
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont("Helvetica-Bold", 9)
    canvas_obj.drawString(2*cm, H_p - 14*mm, "QR Code Tools Management System")
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawRightString(W_p - 2*cm, H_p - 14*mm, "Confidential — Internal Use Only")
    # Footer
    canvas_obj.setFillColor(LIGHT_BG)
    canvas_obj.rect(0, 0, W_p, 15*mm, fill=1, stroke=0)
    canvas_obj.setFillColor(ACCENT)
    canvas_obj.rect(0, 15*mm, W_p, 1, fill=1, stroke=0)
    canvas_obj.setFillColor(colors.grey)
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawString(2*cm, 5*mm, "QR Tools Management System — User Guide")
    canvas_obj.drawRightString(W_p - 2*cm, 5*mm, f"Page {doc.page}")
    canvas_obj.restoreState()


def make_cover(canvas_obj, doc):
    """Cover page — no header/footer."""
    canvas_obj.saveState()
    W_p, H_p = A4

    # Full background gradient simulation
    canvas_obj.setFillColor(PRIMARY)
    canvas_obj.rect(0, 0, W_p, H_p, fill=1, stroke=0)

    # Accent diagonal band
    from reportlab.graphics.shapes import Polygon
    p = canvas_obj.beginPath()
    p.moveTo(0, H_p * 0.35)
    p.lineTo(W_p, H_p * 0.55)
    p.lineTo(W_p, H_p * 0.45)
    p.lineTo(0, H_p * 0.25)
    p.close()
    canvas_obj.setFillColor(ACCENT)
    canvas_obj.setFillAlpha(0.25)
    canvas_obj.drawPath(p, fill=1, stroke=0)
    canvas_obj.setFillAlpha(1)

    # Bottom white section
    canvas_obj.setFillColor(WHITE)
    canvas_obj.rect(0, 0, W_p, H_p * 0.28, fill=1, stroke=0)

    # Company / system name
    canvas_obj.setFillColor(ACCENT)
    canvas_obj.setFont("Helvetica-Bold", 13)
    canvas_obj.drawCentredString(W_p / 2, H_p * 0.82, "QR CODE TOOLS MANAGEMENT SYSTEM")

    # Title
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont("Helvetica-Bold", 28)
    canvas_obj.drawCentredString(W_p / 2, H_p * 0.70, "Complete User Guide")

    # Subtitle
    canvas_obj.setFont("Helvetica", 13)
    canvas_obj.setFillColor(MID_BG)
    canvas_obj.drawCentredString(W_p / 2, H_p * 0.63, "& User Flow Reference")

    # Divider line
    canvas_obj.setStrokeColor(ACCENT)
    canvas_obj.setLineWidth(2)
    canvas_obj.line(4*cm, H_p * 0.58, W_p - 4*cm, H_p * 0.58)

    # Role pills
    roles = ["Admin", "Inspector", "Store Manager", "Worker", "Management", "Data Entry"]
    pill_w = 3.5 * cm
    total = len(roles) * pill_w + (len(roles) - 1) * 0.4 * cm
    x_start = (W_p - total) / 2
    y_pill = H_p * 0.50
    for i, role in enumerate(roles):
        x = x_start + i * (pill_w + 0.4 * cm)
        canvas_obj.setFillColor(ACCENT)
        canvas_obj.setFillAlpha(0.85)
        canvas_obj.roundRect(x, y_pill, pill_w, 14, 7, fill=1, stroke=0)
        canvas_obj.setFillAlpha(1)
        canvas_obj.setFillColor(WHITE)
        canvas_obj.setFont("Helvetica-Bold", 7)
        canvas_obj.drawCentredString(x + pill_w / 2, y_pill + 3, role)

    # Bottom white area — meta info
    canvas_obj.setFillColor(PRIMARY)
    canvas_obj.setFont("Helvetica-Bold", 11)
    canvas_obj.drawCentredString(W_p / 2, H_p * 0.22, "Construction & Industrial Equipment Tracking")
    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.setFillColor(colors.grey)
    canvas_obj.drawCentredString(W_p / 2, H_p * 0.17, "Version 1.0  |  May 2026  |  For Internal Use Only")

    canvas_obj.restoreState()


# ── Style Definitions ─────────────────────────────────────────────────────────

def build_styles():
    base = getSampleStyleSheet()

    body = ParagraphStyle(
        "Body", parent=base["Normal"],
        fontSize=10, leading=15, textColor=colors.black,
        spaceAfter=6, alignment=TA_JUSTIFY,
    )
    body_bold = ParagraphStyle(
        "BodyBold", parent=body, fontName="Helvetica-Bold"
    )
    bullet = ParagraphStyle(
        "Bullet", parent=body,
        leftIndent=18, firstLineIndent=-12,
        spaceBefore=2, spaceAfter=2,
        bulletText="•",
    )
    sub_bullet = ParagraphStyle(
        "SubBullet", parent=bullet,
        leftIndent=36, fontSize=9,
    )
    toc_entry = ParagraphStyle(
        "TOC", parent=base["Normal"],
        fontSize=10, leading=18, textColor=PRIMARY,
    )
    toc_title = ParagraphStyle(
        "TOCTitle", parent=base["Normal"],
        fontSize=18, fontName="Helvetica-Bold",
        textColor=PRIMARY, spaceAfter=16, alignment=TA_CENTER,
    )
    caption = ParagraphStyle(
        "Caption", parent=base["Normal"],
        fontSize=8, textColor=colors.grey, alignment=TA_CENTER,
        spaceAfter=4,
    )
    faq_q = ParagraphStyle(
        "FAQQ", parent=body,
        fontName="Helvetica-Bold", textColor=PRIMARY,
        spaceBefore=10, spaceAfter=2,
    )
    faq_a = ParagraphStyle(
        "FAQA", parent=body,
        leftIndent=10, textColor=colors.black,
    )
    return dict(
        body=body, body_bold=body_bold, bullet=bullet,
        sub_bullet=sub_bullet, toc_entry=toc_entry, toc_title=toc_title,
        caption=caption, faq_q=faq_q, faq_a=faq_a,
    )


# ── Table helpers ─────────────────────────────────────────────────────────────

def make_table(data, col_widths=None, header_bg=TABLE_HEADER):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    n_rows = len(data)
    style = TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0),  header_bg),
        ("TEXTCOLOR",   (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, 0),  9),
        ("FONTNAME",    (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",    (0, 1), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, TABLE_ALT]),
        ("GRID",        (0, 0), (-1, -1), 0.5, FLOW_BORDER),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",  (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ])
    t.setStyle(style)
    return t


def role_table(styles):
    data = [
        ["Role", "Pages Accessible", "Can Edit?"],
        ["Admin",        "All pages",                                  "Yes — full control"],
        ["Data Entry",   "Tool Master (own site only)",                "Yes — create tools only"],
        ["Inspector",    "Inspector View",                             "Yes — inspections only"],
        ["Store Manager","Store View",                                  "Yes — transactions only"],
        ["Worker",       "Worker View",                                 "No — read-only"],
        ["Management",   "Dashboard, Reports, Alerts",                 "No — read-only"],
    ]
    return make_table(data, col_widths=[4*cm, 9*cm, 5.5*cm])


def alert_table(styles):
    data = [
        ["Alert Level", "Colour", "Trigger", "Action Required"],
        ["Critical", "Red",    "Expired tool / Usability <80% / Scrap", "Immediate"],
        ["Warning",  "Yellow", "Expiring within 30 days",               "Within 30 days"],
        ["Info",     "Blue",   "New tool / New user / Pass inspection",  "None"],
    ]
    t = Table(data, colWidths=[3*cm, 2.5*cm, 8.5*cm, 4*cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0),  TABLE_HEADER),
        ("TEXTCOLOR",   (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("BACKGROUND",  (0, 1), (0, 1),   DANGER),
        ("TEXTCOLOR",   (0, 1), (0, 1),   WHITE),
        ("FONTNAME",    (0, 1), (0, 1),   "Helvetica-Bold"),
        ("BACKGROUND",  (0, 2), (0, 2),   WARNING_COL),
        ("FONTNAME",    (0, 2), (0, 2),   "Helvetica-Bold"),
        ("BACKGROUND",  (0, 3), (0, 3),   INFO_COL),
        ("TEXTCOLOR",   (0, 3), (0, 3),   WHITE),
        ("FONTNAME",    (0, 3), (0, 3),   "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, TABLE_ALT]),
        ("GRID",        (0, 0), (-1, -1), 0.5, FLOW_BORDER),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",  (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def transaction_table(styles):
    data = [
        ["Direction", "Type", "When to Use"],
        ["IN",  "subcon_return",  "Subcontractor returning a tool"],
        ["IN",  "new_product",    "Brand new tool arriving for first time"],
        ["IN",  "site_receive",   "Tool transferred from another site"],
        ["OUT", "subcon_work",    "Sending tool to a subcontractor for work"],
        ["OUT", "site_transfer",  "Transferring tool to another site"],
    ]
    t = Table(data, colWidths=[2.5*cm, 4.5*cm, 11.5*cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0),  TABLE_HEADER),
        ("TEXTCOLOR",   (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("BACKGROUND",  (0, 1), (0, 3),   HexColor("#D5F5E3")),
        ("TEXTCOLOR",   (0, 1), (0, 3),   SUCCESS),
        ("FONTNAME",    (0, 1), (0, 3),   "Helvetica-Bold"),
        ("BACKGROUND",  (0, 4), (0, 5),   HexColor("#FDEDEC")),
        ("TEXTCOLOR",   (0, 4), (0, 5),   DANGER),
        ("FONTNAME",    (0, 4), (0, 5),   "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, TABLE_ALT]),
        ("GRID",        (0, 0), (-1, -1), 0.5, FLOW_BORDER),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",  (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def split_result_table(styles):
    data = [
        ["Result", "Indicator", "Meaning", "Action"],
        ["Correct Combination", "GREEN",  "Parts match, both Usable",          "Safe to use"],
        ["Mixed Status",        "YELLOW", "Parts match, one/both not fully usable", "Caution — report to supervisor"],
        ["Mismatch",            "RED",    "Description or site don't match",   "STOP — Wrong combination"],
    ]
    t = Table(data, colWidths=[4.5*cm, 2.5*cm, 7*cm, 4.5*cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0),  TABLE_HEADER),
        ("TEXTCOLOR",   (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("BACKGROUND",  (0, 1), (-1, 1),  HexColor("#D5F5E3")),
        ("BACKGROUND",  (0, 2), (-1, 2),  HexColor("#FEF9E7")),
        ("BACKGROUND",  (0, 3), (-1, 3),  HexColor("#FDEDEC")),
        ("TEXTCOLOR",   (1, 1), (1, 1),   SUCCESS),
        ("FONTNAME",    (1, 1), (1, 1),   "Helvetica-Bold"),
        ("TEXTCOLOR",   (1, 2), (1, 2),   WARNING_COL),
        ("FONTNAME",    (1, 2), (1, 2),   "Helvetica-Bold"),
        ("TEXTCOLOR",   (1, 3), (1, 3),   DANGER),
        ("FONTNAME",    (1, 3), (1, 3),   "Helvetica-Bold"),
        ("TEXTCOLOR",   (0, 3), (0, 3),   DANGER),
        ("FONTNAME",    (0, 3), (0, 3),   "Helvetica-Bold"),
        ("GRID",        (0, 0), (-1, -1), 0.5, FLOW_BORDER),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",  (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def bulk_columns_table(styles):
    data = [
        ["Column Name", "Required?", "Example Value", "Notes"],
        ["description",        "YES", "Clamp Head",    "Name of the tool"],
        ["make",               "YES", "2022",          "Year or manufacturer"],
        ["capacity",           "YES", "8 Ton",         "Load capacity"],
        ["safe_working_load",  "YES", "8 Ton",         "Maximum safe load"],
        ["purchaser_name",     "YES", "ABC Corp",      "Who purchased the tool"],
        ["supplier_code",      "No",  "SUP001",        "Supplier reference"],
        ["date_of_supply",     "No",  "2024-01-15",    "Format: YYYY-MM-DD"],
        ["tool_type",          "No",  "Erection Tools","Erection or Stringing"],
        ["metal_type",         "No",  "Steel",         "Material"],
        ["tool_variant",       "No",  "Type A",        "Specific model/variant"],
        ["purchaser_contact",  "No",  "+1234567890",   "Phone number"],
        ["job_code",           "No",  "JOB-001",       "Project reference"],
        ["job_description",    "No",  "Tower Erection","Project description"],
        ["location",           "No",  "Site A",        "Current site name"],
    ]
    t = Table(data, colWidths=[4.5*cm, 2*cm, 5*cm, 7*cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0),  TABLE_HEADER),
        ("TEXTCOLOR",   (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 8.5),
        ("TEXTCOLOR",   (1, 1), (1, 5),   SUCCESS),
        ("FONTNAME",    (1, 1), (1, 5),   "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, TABLE_ALT]),
        ("GRID",        (0, 0), (-1, -1), 0.5, FLOW_BORDER),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


# ── Flow Box Factory ──────────────────────────────────────────────────────────

def flow(lines):
    return FlowBox(lines)


# ── TOC Page ─────────────────────────────────────────────────────────────────

def build_toc(styles, story):
    story.append(Paragraph("Table of Contents", styles["toc_title"]))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT))
    story.append(Spacer(1, 10))

    entries = [
        ("1",  "System Overview"),
        ("2",  "User Roles & Access Control"),
        ("3",  "Getting Started — Login Flow"),
        ("4",  "Admin Guide — Tool Master"),
        ("4.1","  Creating a New Tool"),
        ("4.2","  Viewing & Editing Tools"),
        ("4.3","  Printing QR Codes"),
        ("5",  "Admin Guide — Dashboard"),
        ("6",  "Admin Guide — Alerts"),
        ("7",  "Admin Guide — Users Management"),
        ("8",  "Admin Guide — Reports"),
        ("9",  "Inspector User Guide"),
        ("10", "Store Manager User Guide"),
        ("11", "Worker User Guide"),
        ("12", "Split Tool Matching"),
        ("13", "Bulk Import Guide"),
        ("14", "Complete System Flow Diagram"),
        ("15", "Frequently Asked Questions"),
    ]
    for num, title in entries:
        indent = 20 if num.count(".") else 0
        dot_leader = "." * 80
        text = f"<font color='#{PRIMARY.hexval()[2:]}' name='Helvetica-Bold'>{num}</font>"
        p = Paragraph(
            f"<font name='Helvetica-Bold' color='#{PRIMARY.hexval()[2:]}'>{num}</font>"
            f"&nbsp;&nbsp;<font color='#1E3A5F'>{title}</font>",
            ParagraphStyle("toc_item", parent=styles["toc_entry"],
                           leftIndent=indent, spaceBefore=3)
        )
        story.append(p)
    story.append(PageBreak())


# ── Main Build ────────────────────────────────────────────────────────────────

def build_pdf():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title="QR Code Tools Management System — User Guide",
        author="QR Tools System",
    )

    styles = build_styles()
    story  = []

    # ── COVER ──
    story.append(Spacer(1, H * 0.55))  # placeholder; cover drawn via onFirstPage
    story.append(PageBreak())

    # ── TOC ──
    build_toc(styles, story)

    sp = lambda n=8: Spacer(1, n)

    # ─────────────────────────────────────────────────────────────
    # SECTION 1 — SYSTEM OVERVIEW
    # ─────────────────────────────────────────────────────────────
    story.append(SectionBanner("System Overview", 1))
    story.append(sp(12))
    story.append(Paragraph(
        "The QR Code Tools Management System is a digital platform for tracking construction "
        "and industrial tools across multiple job sites. It replaces manual paper logs with a "
        "smart, scannable, role-based system that keeps every stakeholder informed in real time.",
        styles["body"]
    ))
    story.append(sp(6))
    story.append(SubHeading("Core Capabilities"))
    story.append(sp(6))
    caps = [
        ("Track Tools",       "Know where every tool is, its condition, and who last used it."),
        ("Scan QR Codes",     "Instantly pull up any tool's details by scanning its QR sticker."),
        ("Run Inspections",   "Record safety checks with photos and usability ratings."),
        ("Move Tools",        "Log when tools move between sites and subcontractors."),
        ("Get Alerts",        "Automatic warnings for expired or damaged tools."),
        ("Generate Reports",  "Export tool lists and certificates as Excel or PDF."),
        ("Match Split Tools", "Verify that Part A and Part B of a tool belong together."),
        ("Bulk Import",       "Upload Excel files to register many tools at once."),
    ]
    cap_data = [["Capability", "Description"]] + [[f"  {c}", d] for c, d in caps]
    story.append(make_table(cap_data, col_widths=[5*cm, 13.5*cm]))
    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # SECTION 2 — USER ROLES
    # ─────────────────────────────────────────────────────────────
    story.append(SectionBanner("User Roles & Access Control", 2))
    story.append(sp(12))
    story.append(Paragraph(
        "Each user is assigned a role that controls which pages they can access and what actions "
        "they can perform. After login, users are automatically redirected to their role-specific page.",
        styles["body"]
    ))
    story.append(sp(8))
    story.append(role_table(styles))
    story.append(sp(10))
    story.append(AlertBox(
        "IMPORTANT",
        "Contact your system administrator if you need access to pages not listed for your role.",
        kind="note"
    ))
    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # SECTION 3 — LOGIN FLOW
    # ─────────────────────────────────────────────────────────────
    story.append(SectionBanner("Getting Started — Login Flow", 3))
    story.append(sp(12))
    story.append(Paragraph(
        "Open your browser and navigate to the system URL provided by your administrator "
        "(e.g., <font name='Courier'>http://192.168.x.x:5173</font>). "
        "You will be greeted by the login screen.",
        styles["body"]
    ))
    story.append(sp(8))
    story.append(SubHeading("User Flow — Login Process"))
    story.append(sp(6))
    story.append(flow([
        "Step 1:  Open browser → Navigate to system URL",
        "Step 2:  Login screen appears",
        "Step 3:  Enter Username and Password",
        "Step 4:  Click [Sign In]",
        "         ┌─────────────────────────────────────────────┐",
        "         │  Valid credentials?                         │",
        "         │  YES → JWT token issued → Redirect to role  │",
        "         │  NO  → Error message shown → Retry          │",
        "         └─────────────────────────────────────────────┘",
        "Alternative: Scan your personal QR code to authenticate",
    ]))
    story.append(sp(10))
    story.append(AlertBox(
        "TIP",
        "If you cannot log in, contact your admin to verify your account is Active.",
        kind="info"
    ))
    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # SECTION 4 — ADMIN — TOOL MASTER
    # ─────────────────────────────────────────────────────────────
    story.append(SectionBanner("Admin Guide — Tool Master", 4))
    story.append(sp(12))
    story.append(Paragraph(
        "The Tool Master is the central hub for creating, viewing, and editing all tool records. "
        "It contains three tabs: New Entry, Saved Tools, and Import.",
        styles["body"]
    ))
    story.append(sp(8))

    # 4.1
    story.append(SubHeading("4.1  Creating a New Tool"))
    story.append(sp(6))
    story.append(flow([
        "Step 1:  Click 'Tool Master' in the sidebar",
        "Step 2:  Select the 'New Entry' tab",
        "Step 3:  Fill in the form (see field table below)",
        "Step 4:  Upload Test Certificate (PDF/JPG/PNG) — optional",
        "Step 5:  Click [Save Tool]",
        "Step 6:  System auto-generates a unique QR code",
        "Step 7:  'New Tool Added' info alert is created automatically",
        "Step 8:  QR code displayed — print or download",
    ]))
    story.append(sp(8))

    fields_data = [
        ["Field", "What to Enter", "Required?"],
        ["Description",         "Name of the tool (e.g., Clamp Head)",       "YES"],
        ["Make / Year",         "Manufacturer or year of manufacture",        "YES"],
        ["Capacity",            "Load capacity (e.g., 8 Ton)",                "YES"],
        ["Safe Working Load",   "Maximum safe load rating",                   "YES"],
        ["Tool Type",           "Erection Tools or Stringing Tools",          "YES"],
        ["Metal Type",          "Material the tool is made from",             "YES"],
        ["Tool Variant",        "Specific variant or model",                  "YES"],
        ["Purchaser Name",      "Who purchased the tool",                     "YES"],
        ["Purchaser Contact",   "Purchaser phone number",                     "No"],
        ["Supplier Code",       "Supplier reference number",                  "No"],
        ["Date of Supply",      "When the tool was received (YYYY-MM-DD)",    "YES"],
        ["Validity Period",     "How many years the tool is certified for",   "YES"],
        ["Test Certificate",    "Upload PDF or image file",                   "No"],
        ["Current Site",        "Where the tool is located now",              "YES"],
        ["Subcontractor Name",  "Name of the subcontractor (if applicable)",  "No"],
        ["Subcontractor Code",  "Subcontractor reference code",               "No"],
        ["Subcontractor Mobile","Subcontractor phone number",                 "No"],
        ["Job Code",            "Project reference code",                     "No"],
        ["Job Description",     "Project description",                        "No"],
        ["Remarks",             "Any additional notes",                       "No"],
    ]
    t = Table(fields_data, colWidths=[4.5*cm, 9.5*cm, 4.5*cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0),  TABLE_HEADER),
        ("TEXTCOLOR",   (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 8.5),
        ("TEXTCOLOR",   (2, 1), (2, 8),   SUCCESS),
        ("FONTNAME",    (2, 1), (2, 8),   "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, TABLE_ALT]),
        ("GRID",        (0, 0), (-1, -1), 0.5, FLOW_BORDER),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(sp(10))

    story.append(SubHeading("QR Code Auto-Generation Logic"))
    story.append(sp(6))
    story.append(flow([
        "The system builds each QR code automatically from the tool's data:",
        "",
        "  Name Part    : First 2 letters of description  (e.g., 'CL' for Clamp)",
        "  Metal Part   : First letter of metal type       (e.g., 'S' for Steel)",
        "  Variant Part : Initials of each word in variant (e.g., 'TA' for Type A)",
        "  Capacity Part: Numeric digits from capacity     (e.g., '8' from '8 Ton')",
        "  Date Part    : MM-YY from date of supply        (e.g., '01-24')",
        "  Supplier Part: First 2 letters of purchaser     (e.g., 'AB' for ABC Corp)",
        "  Serial Part  : 4-digit auto-incremented number  (e.g., '0101')",
        "",
        "  Example result:  CLSTA8-01-24AB0101",
        "  Uniqueness guaranteed — system appends '-1', '-2' if duplicate found.",
    ]))
    story.append(PageBreak())

    # 4.2
    story.append(SubHeading("4.2  Viewing & Editing Tools"))
    story.append(sp(6))
    story.append(flow([
        "Step 1:  Go to Tool Master → 'Saved Tools' tab",
        "Step 2:  Use the search bar to find by any field",
        "         OR use the Site / Creator filter dropdowns",
        "Step 3:  Click a tool row to view full details",
        "Step 4:  Click the Edit icon to modify the tool",
        "Step 5:  Make your changes and click Save",
        "         NOTE: If the site field changes, a movement history entry",
        "               is recorded automatically",
        "Step 6:  Confirmation message displayed",
    ]))
    story.append(sp(10))

    # 4.3
    story.append(SubHeading("4.3  Printing QR Codes"))
    story.append(sp(6))
    story.append(flow([
        "Step 1:  Go to Tool Master → Saved Tools tab",
        "Step 2:  Find the tool in the table",
        "Step 3:  Click the QR icon on that row",
        "Step 4:  QR code image appears in a modal popup",
        "Step 5:  Click Print or Save Image",
        "Step 6:  Print the label and stick it on the physical tool",
    ]))
    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # SECTION 5 — DASHBOARD
    # ─────────────────────────────────────────────────────────────
    story.append(SectionBanner("Admin Guide — Dashboard", 5))
    story.append(sp(12))
    story.append(Paragraph(
        "The Dashboard provides a real-time snapshot of your entire tool inventory through "
        "summary cards and interactive charts.",
        styles["body"]
    ))
    story.append(sp(8))
    story.append(SubHeading("Summary Metric Cards"))
    story.append(sp(6))
    cards_data = [
        ["Card",            "Meaning"],
        ["Total Tools",     "All tools registered in the system"],
        ["Usable",          "Tools currently in good working condition"],
        ["Scrap",           "Tools retired after a failed inspection"],
        ["Expiring Soon",   "Tools whose certification expires within 30 days"],
        ["Overdue",         "Tools whose certification has already expired"],
    ]
    story.append(make_table(cards_data, col_widths=[5*cm, 13.5*cm]))
    story.append(sp(8))
    story.append(SubHeading("Available Charts"))
    story.append(sp(6))
    charts_data = [
        ["Chart",                    "Type",      "What It Shows"],
        ["Tools by Site",            "Bar",       "How many tools are at each location"],
        ["Status Distribution",      "Pie",       "Usable vs. Scrap split"],
        ["Inspection Trends",        "Line",      "Number of inspections over time"],
        ["Tool Age Distribution",    "Bar",       "Breakdown of tool ages"],
        ["At-Risk Tools",            "List/Bar",  "Tools with low usability or near expiry"],
    ]
    story.append(make_table(charts_data, col_widths=[5.5*cm, 2.5*cm, 10.5*cm]))
    story.append(sp(8))
    story.append(SubHeading("User Flow — Using the Dashboard"))
    story.append(sp(6))
    story.append(flow([
        "Step 1:  Click 'Dashboard' in the sidebar",
        "Step 2:  Review the five summary cards at the top",
        "Step 3:  (Optional) Select a filter: by User or by Site",
        "Step 4:  Review charts for trends and problem areas",
        "Step 5:  Click 'Export' to download a data snapshot",
    ]))
    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # SECTION 6 — ALERTS
    # ─────────────────────────────────────────────────────────────
    story.append(SectionBanner("Admin Guide — Alerts", 6))
    story.append(sp(12))
    story.append(Paragraph(
        "The Alerts system automatically monitors all tools and notifies administrators "
        "when action is required. Alerts are sorted by severity — most critical first.",
        styles["body"]
    ))
    story.append(sp(8))
    story.append(SubHeading("Alert Types & Severity"))
    story.append(sp(6))
    story.append(alert_table(styles))
    story.append(sp(8))
    story.append(SubHeading("When Are Alerts Triggered?"))
    story.append(sp(6))
    triggers_data = [
        ["Alert",                "Triggered When"],
        ["New Tool Added",       "A tool record is created in the system"],
        ["New User Created",     "A user account is added"],
        ["Tool Expiring Soon",   "Expiry date is within 30 days of today"],
        ["Tool Expired",         "Expiry date has already passed"],
        ["Low Usability",        "Inspection usability result is below 80%"],
        ["Tool Scrapped",        "A tool is marked as Scrap after inspection"],
    ]
    story.append(make_table(triggers_data, col_widths=[5*cm, 13.5*cm]))
    story.append(sp(8))
    story.append(SubHeading("User Flow — Managing Alerts"))
    story.append(sp(6))
    story.append(flow([
        "Step 1:  Click 'Alerts' in the sidebar",
        "Step 2:  Alerts displayed grouped by severity (Critical first)",
        "Step 3:  Review all RED (Critical) alerts first",
        "Step 4:  Click any alert to see full details:",
        "         - Tool ID and description",
        "         - Site location",
        "         - Timestamp of trigger",
        "Step 5:  Take appropriate action:",
        "         Critical → Withdraw tool / Schedule immediate inspection",
        "         Warning  → Plan inspection or replacement within 30 days",
        "         Info     → No action needed",
    ]))
    story.append(sp(8))
    story.append(AlertBox(
        "SAFETY NOTE",
        "Critical alerts indicate tools that pose a safety risk. Never ignore red alerts.",
        kind="critical"
    ))
    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # SECTION 7 — USERS MANAGEMENT
    # ─────────────────────────────────────────────────────────────
    story.append(SectionBanner("Admin Guide — Users Management", 7))
    story.append(sp(12))
    story.append(Paragraph(
        "Admins manage all user accounts from the Users page. You can add, edit, "
        "deactivate, or delete users.",
        styles["body"]
    ))
    story.append(sp(8))
    story.append(SubHeading("User Flow — Add a New User"))
    story.append(sp(6))
    story.append(flow([
        "Step 1:  Click 'Users' in the sidebar",
        "Step 2:  Click the [Add User] button",
        "Step 3:  Fill in:",
        "         - Full Name",
        "         - Username (unique login name)",
        "         - Email address (validated format)",
        "         - Phone number",
        "         - Password",
        "         - Role (Admin/Inspector/Store/Worker/Management/Data Entry)",
        "         - Assigned Site",
        "Step 4:  Click Save",
        "Step 5:  System creates the account and triggers a 'New User' info alert",
        "Step 6:  User appears in the list and can now log in",
    ]))
    story.append(sp(8))
    story.append(SubHeading("User Flow — Deactivate a User"))
    story.append(sp(6))
    story.append(flow([
        "Step 1:  Find the user in the list",
        "Step 2:  Toggle the Active/Inactive switch to INACTIVE",
        "Step 3:  User immediately loses login access",
        "         NOTE: Account and all history are preserved (not deleted)",
        "Step 4:  Toggle back to ACTIVE to restore access",
    ]))
    story.append(sp(8))
    story.append(SubHeading("User Flow — Delete a User"))
    story.append(sp(6))
    story.append(flow([
        "Step 1:  Find the user in the list",
        "Step 2:  Click the Delete icon",
        "Step 3:  Confirm the deletion in the dialog",
        "Step 4:  User is permanently removed (Admin only)",
        "         WARNING: This action cannot be undone",
    ]))
    story.append(sp(8))
    story.append(AlertBox(
        "RECOMMENDATION",
        "Prefer Deactivating users over Deleting them to preserve audit history.",
        kind="warning"
    ))
    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # SECTION 8 — REPORTS
    # ─────────────────────────────────────────────────────────────
    story.append(SectionBanner("Admin Guide — Reports", 8))
    story.append(sp(12))
    story.append(Paragraph(
        "The Reports page lets you search across all tool data and export the results "
        "as a CSV file compatible with Excel or Google Sheets.",
        styles["body"]
    ))
    story.append(sp(8))
    story.append(SubHeading("User Flow — Exporting a Report"))
    story.append(sp(6))
    story.append(flow([
        "Step 1:  Click 'Reports' in the sidebar",
        "Step 2:  Type in the search box to filter by any field",
        "         (description, QR code, site, subcontractor, etc.)",
        "Step 3:  Use column filter dropdowns to narrow results further",
        "Step 4:  Hover over any row to see the QR code preview",
        "Step 5:  Click [Download CSV]",
        "Step 6:  CSV file saved to your computer",
        "         (Opens in Excel, Google Sheets, or any spreadsheet app)",
    ]))
    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # SECTION 9 — INSPECTOR
    # ─────────────────────────────────────────────────────────────
    story.append(SectionBanner("Inspector User Guide", 9))
    story.append(sp(12))
    story.append(Paragraph(
        "Inspectors are automatically taken to the Inspector View after login. "
        "This is the only page available to this role. Your job is to find tools and "
        "record their safety inspection results.",
        styles["body"]
    ))
    story.append(sp(8))
    story.append(SubHeading("User Flow — Complete a Safety Inspection"))
    story.append(sp(6))
    story.append(flow([
        "Step 1:  Inspector View opens automatically after login",
        "",
        "Step 2:  Find the tool using ONE of these methods:",
        "         a) Camera Scan  — Click camera icon, point at QR sticker",
        "         b) Upload Image — Photograph the QR sticker, upload the photo",
        "         c) Manual Search— Type the QR code or tool ID in search box",
        "",
        "Step 3:  System fetches and displays tool details:",
        "         - Description, Make, Capacity, SWL",
        "         - Current site, Status, Last inspection date",
        "",
        "Step 4:  Physically review the tool",
        "",
        "Step 5:  Fill in the Inspection Form:",
        "         - Result         : Pass / Conditional / Fail",
        "         - Usability %    : Drag slider 0-100",
        "         - Photos         : Upload damage/condition photos",
        "         - Remarks        : Write your observations",
        "",
        "Step 6:  Click [Submit Inspection]",
    ]))
    story.append(sp(8))
    story.append(SubHeading("What Happens Automatically After Submission"))
    story.append(sp(6))
    auto_data = [
        ["Condition", "Automatic Action"],
        ["Any result",        "last_inspection_date updated to today"],
        ["Any result",        "usability_percentage updated to entered value"],
        ["Result = Fail",     "tool.status changed to 'Scrap' immediately"],
        ["Usability < 80%",   "Critical alert created for admin"],
        ["Result = Pass",     "Confirmation message shown — no further action"],
    ]
    t2 = Table(auto_data, colWidths=[6*cm, 12.5*cm], repeatRows=1)
    t2.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0),  TABLE_HEADER),
        ("TEXTCOLOR",   (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("BACKGROUND",  (0, 3), (-1, 3),  HexColor("#FDEDEC")),
        ("BACKGROUND",  (0, 4), (-1, 4),  HexColor("#FEF9E7")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, TABLE_ALT]),
        ("GRID",        (0, 0), (-1, -1), 0.5, FLOW_BORDER),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",  (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t2)
    story.append(sp(8))
    story.append(SubHeading("Inspection Decision Flow"))
    story.append(sp(6))
    story.append(flow([
        "                   [ Inspect Tool ]",
        "                         |",
        "         ┌───────────────┼───────────────┐",
        "         |               |               |",
        "       PASS         CONDITIONAL         FAIL",
        "         |               |               |",
        "   Usability?       Record saved     Tool = SCRAP",
        "   /       \\        Tool = Usable    Alert created",
        ">=80%    <80%",
        "  |         |",
        "Saved   Saved +",
        "        CRITICAL",
        "        alert",
    ]))
    story.append(sp(8))
    story.append(AlertBox(
        "IMPORTANT",
        "A Fail result permanently marks the tool as Scrap. Double-check before selecting Fail.",
        kind="critical"
    ))
    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # SECTION 10 — STORE MANAGER
    # ─────────────────────────────────────────────────────────────
    story.append(SectionBanner("Store Manager User Guide", 10))
    story.append(sp(12))
    story.append(Paragraph(
        "Store Managers are automatically taken to the Store View after login. "
        "Your job is to record all tool movements into and out of your store location.",
        styles["body"]
    ))
    story.append(sp(8))
    story.append(SubHeading("User Flow — Record a Tool Transaction"))
    story.append(sp(6))
    story.append(flow([
        "Step 1:  Store View opens automatically after login",
        "Step 2:  Scan the tool QR code using camera",
        "         OR type the QR code manually in the search box",
        "Step 3:  System displays tool details and last transaction",
        "Step 4:  Select Transaction Direction: IN or OUT",
        "Step 5:  Select Transaction Type (see table below)",
        "Step 6:  Fill in additional details:",
        "         - Subcontractor Name, Code, Mobile (if applicable)",
        "         - Target Site (where the tool is going)",
        "         - Remarks (optional)",
        "Step 7:  Click [Record Movement]",
        "Step 8:  System updates tool's current site and records history",
        "Step 9:  Last transaction confirmation displayed on screen",
    ]))
    story.append(sp(8))
    story.append(SubHeading("Transaction Types"))
    story.append(sp(6))
    story.append(transaction_table(styles))
    story.append(sp(8))
    story.append(SubHeading("User Flow — Incident Mode"))
    story.append(sp(6))
    story.append(flow([
        "Use Incident Mode when recording a damaged or missing tool.",
        "",
        "Step 1:  Toggle 'Incident Mode' ON before scanning the tool",
        "Step 2:  Scan the tool as normal",
        "Step 3:  Enter the 'Debit To' code (person/team responsible)",
        "Step 4:  Record movement as normal",
        "Step 5:  An alert is created for the admin automatically",
    ]))
    story.append(sp(8))
    story.append(AlertBox(
        "NOTE",
        "Every movement is logged with your name, the tool, and a timestamp for full audit trail.",
        kind="info"
    ))
    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # SECTION 11 — WORKER
    # ─────────────────────────────────────────────────────────────
    story.append(SectionBanner("Worker User Guide", 11))
    story.append(sp(12))
    story.append(Paragraph(
        "Workers are automatically taken to the Worker View after login. "
        "This is a read-only view — no changes can be made. "
        "Use it to check a tool's status and safety information before use.",
        styles["body"]
    ))
    story.append(sp(8))
    story.append(SubHeading("User Flow — Check a Tool"))
    story.append(sp(6))
    story.append(flow([
        "Step 1:  Worker View opens automatically after login",
        "Step 2:  Click the [Scan] button",
        "Step 3:  Point your camera at the tool's QR sticker",
        "Step 4:  System displays all tool information:",
        "         - Description & Make",
        "         - Capacity & Safe Working Load (SWL)",
        "         - Current Site",
        "         - Status: USABLE (green) or SCRAP (red)",
        "         - Usability %",
        "         - Expiry Date",
        "         - Subcontractor Info",
    ]))
    story.append(sp(8))
    story.append(SubHeading("Worker Decision Guide"))
    story.append(sp(6))
    decision_data = [
        ["Status",                     "Usability",  "Decision"],
        ["USABLE",                     ">= 80%",     "Safe to use"],
        ["USABLE",                     "< 80%",      "Use with caution — report to supervisor"],
        ["SCRAP",                      "Any",        "DO NOT USE — Report to supervisor immediately"],
        ["USABLE (Expired)",           "Any",        "DO NOT USE — Certification expired"],
    ]
    t3 = Table(decision_data, colWidths=[5*cm, 3*cm, 10.5*cm], repeatRows=1)
    t3.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0),  TABLE_HEADER),
        ("TEXTCOLOR",   (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("BACKGROUND",  (0, 1), (-1, 1),  HexColor("#D5F5E3")),
        ("BACKGROUND",  (0, 2), (-1, 2),  HexColor("#FEF9E7")),
        ("BACKGROUND",  (0, 3), (-1, 3),  HexColor("#FDEDEC")),
        ("BACKGROUND",  (0, 4), (-1, 4),  HexColor("#FDEDEC")),
        ("TEXTCOLOR",   (2, 3), (2, 3),   DANGER),
        ("FONTNAME",    (2, 3), (2, 3),   "Helvetica-Bold"),
        ("TEXTCOLOR",   (2, 4), (2, 4),   DANGER),
        ("FONTNAME",    (2, 4), (2, 4),   "Helvetica-Bold"),
        ("GRID",        (0, 0), (-1, -1), 0.5, FLOW_BORDER),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",  (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t3)
    story.append(sp(8))
    story.append(AlertBox(
        "SAFETY RULE",
        "If the tool shows SCRAP or an expired date — stop and report it to your supervisor immediately.",
        kind="critical"
    ))
    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # SECTION 12 — SPLIT TOOL
    # ─────────────────────────────────────────────────────────────
    story.append(SectionBanner("Split Tool Matching", 12))
    story.append(sp(12))
    story.append(Paragraph(
        "Some tools consist of two parts (Part A + Part B) that must be used together. "
        "The Split Tool Matching feature verifies that you have the correct matching pair "
        "before use.",
        styles["body"]
    ))
    story.append(sp(8))
    story.append(SubHeading("User Flow — Match a Split Tool"))
    story.append(sp(6))
    story.append(flow([
        "Step 1:  Navigate to the Split Tool page",
        "",
        "Step 2:  Scan Part A:",
        "         → Click [Scan Part A]",
        "         → Scan or upload the QR code from the first component",
        "         → Part A details displayed on screen",
        "",
        "Step 3:  Scan Part B:",
        "         → Click [Scan Part B]",
        "         → Scan or upload the QR code from the second component",
        "         → Part B details displayed on screen",
        "",
        "Step 4:  System automatically compares:",
        "         ✓ Description match?",
        "         ✓ Current site match?",
        "         ✓ Make match?",
        "         ✓ Capacity & SWL match?",
        "",
        "Step 5:  Result displayed with colour indicator",
    ]))
    story.append(sp(8))
    story.append(SubHeading("Matching Results"))
    story.append(sp(6))
    story.append(split_result_table(styles))
    story.append(sp(8))
    story.append(AlertBox(
        "SAFETY RULE",
        "Never use a RED (Mismatch) combination. Always confirm GREEN before use.",
        kind="critical"
    ))
    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # SECTION 13 — BULK IMPORT
    # ─────────────────────────────────────────────────────────────
    story.append(SectionBanner("Bulk Import Guide", 13))
    story.append(sp(12))
    story.append(Paragraph(
        "Use bulk import to register many tools at once by uploading an Excel file, "
        "instead of entering them one by one. The system will automatically generate "
        "QR codes for every imported tool.",
        styles["body"]
    ))
    story.append(sp(8))
    story.append(SubHeading("User Flow — Bulk Import Tools"))
    story.append(sp(6))
    story.append(flow([
        "Step 1:  Go to Tool Master → 'Import' tab",
        "Step 2:  Click [Download Template] to get the Excel template file",
        "Step 3:  Open the file in Excel or Google Sheets",
        "Step 4:  Enter one tool per row (see column guide below)",
        "Step 5:  Save the file",
        "Step 6:  Back in the system — click [Upload File]",
        "Step 7:  Select your completed Excel or PDF file",
        "Step 8:  Click [Import]",
        "Step 9:  System processes each row:",
        "         → Validates required fields",
        "         → Generates a unique QR code per tool",
        "         → Creates each Tool record in the database",
        "Step 10: Download your results:",
        "         → QR Code ZIP  : PNG images of all QR codes, ready to print",
        "         → Excel + QR   : Original file with 'qr_link' column added",
        "Step 11: Any failed rows are listed with the reason — fix and re-upload",
    ]))
    story.append(sp(8))
    story.append(SubHeading("Excel Column Reference"))
    story.append(sp(6))
    story.append(bulk_columns_table(styles))
    story.append(sp(8))
    story.append(SubHeading("Common Import Errors"))
    story.append(sp(6))
    err_data = [
        ["Error",                  "Cause",                          "Fix"],
        ["Missing required field", "Column left blank for a row",    "Fill in the missing value"],
        ["Invalid date format",    "Date not in YYYY-MM-DD format",  "Change to e.g. 2024-01-15"],
        ["Duplicate entry",        "Tool already exists in system",  "Remove the duplicate row"],
    ]
    story.append(make_table(err_data, col_widths=[5*cm, 6*cm, 7.5*cm]))
    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # SECTION 14 — SYSTEM FLOW DIAGRAM
    # ─────────────────────────────────────────────────────────────
    story.append(SectionBanner("Complete System Flow Diagram", 14))
    story.append(sp(12))
    story.append(SubHeading("Overall Tool Lifecycle Flow"))
    story.append(sp(6))
    story.append(flow([
        "  [Tool Created / Bulk Imported by Admin or Data Entry]",
        "                           |",
        "                           v",
        "          [QR Code Auto-Generated & Printed]",
        "                           |",
        "                           v",
        "       [QR Sticker Applied to Physical Tool]",
        "                           |",
        "                           v",
        "           [Tool Dispatched to Job Site]",
        "                           |",
        "                           v",
        "  [Store Manager records OUT transaction in Store View]",
        "                           |",
        "                           v",
        "              [Tool in Use at Site]",
        "                           |",
        "                           v",
        "  [Inspector performs periodic safety inspection]",
        "                           |",
        "          +----------------+----------------+",
        "          |                                 |",
        "        PASS                              FAIL",
        "          |                                 |",
        "   Tool continues                  Tool status = SCRAP",
        "   in service                      Critical alert sent",
        "          |                        Tool withdrawn from use",
        "          v",
        "  [Tool returned to store]",
        "          |",
        "          v",
        "  [Store Manager records IN transaction]",
        "          |",
        "          v",
        "  [Tool available for re-issue or retirement]",
    ]))
    story.append(sp(10))
    story.append(SubHeading("Alert Monitoring Flow (Continuous)"))
    story.append(sp(6))
    story.append(flow([
        "  System continuously monitors all tools:",
        "",
        "   Expiry date within 30 days?  →  WARNING alert created",
        "   Expiry date has passed?       →  CRITICAL alert created",
        "   Usability < 80%?              →  CRITICAL alert created",
        "   Tool status = Scrap?          →  CRITICAL alert created",
        "   New tool added?               →  INFO alert created",
        "   New user added?               →  INFO alert created",
        "",
        "  Admin reviews alerts daily:",
        "   CRITICAL  →  Immediate action — withdraw / replace tool",
        "   WARNING   →  Schedule action within 30 days",
        "   INFO      →  No action required",
    ]))
    story.append(sp(10))
    story.append(SubHeading("Login & Role Routing Flow"))
    story.append(sp(6))
    story.append(flow([
        "  User opens browser → System URL",
        "        |",
        "   Enters credentials",
        "        |",
        "   +---------+-----------+---------+---------+-----------+",
        "   |         |           |         |         |           |",
        " Admin    Inspector   Store      Worker  Management  Data Entry",
        "   |         |         Mgr          |         |           |",
        " All      Inspector  Store       Worker   Dashboard   Tool Master",
        " Pages    View       View        View     Reports     (own site)",
        "                                          Alerts",
    ]))
    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # SECTION 15 — FAQ
    # ─────────────────────────────────────────────────────────────
    story.append(SectionBanner("Frequently Asked Questions", 15))
    story.append(sp(12))

    faqs = [
        ("I can't log in. What do I do?",
         "Contact your admin to verify your username and password are correct, "
         "and that your account is set to Active status."),

        ("The QR scan isn't working. What should I try?",
         "(1) Make sure your browser has camera permission. "
         "(2) Try the 'Upload Image' option — photograph the QR sticker and upload the photo. "
         "(3) If the code is damaged or too small, type it manually in the search box."),

        ("A tool shows as Scrap but it's still usable. Can I change it?",
         "Only an Admin can update a tool's status. Contact your administrator "
         "to review and correct the record after verifying the tool's actual condition."),

        ("I made a mistake when adding a tool. Can I fix it?",
         "Yes. Go to Tool Master → Saved Tools, find the tool, click the Edit icon, "
         "make your corrections, and save."),

        ("The wrong QR code is on a physical tool. What do I do?",
         "Find the correct tool record in Saved Tools. Print the correct QR code from that record. "
         "Peel off the wrong sticker and replace it with the printed correct one."),

        ("How do I know if two tool parts belong together?",
         "Use the Split Tool Matching feature. Scan both Part A and Part B. "
         "The system tells you instantly if they are a correct combination (green), "
         "mixed status (yellow), or a mismatch (red)."),

        ("My bulk import has errors. What do I do?",
         "After import, the system lists every row that failed and explains why. "
         "Fix those rows in your Excel file and re-upload only the failed rows."),

        ("Can I use this system on my phone?",
         "Yes. Open the system URL in Chrome or Safari on your phone. "
         "The QR scanning feature uses your phone's camera directly."),

        ("How long are tool records kept?",
         "Tool records, inspection history, and movement logs are kept indefinitely. "
         "Admins can export a PDF report covering the last 12 months of activity."),

        ("What happens when I submit a Fail inspection?",
         "The tool is automatically marked as Scrap and a Critical alert is sent to the admin. "
         "The tool must be withdrawn from service immediately. "
         "This action cannot be undone by an inspector — contact an admin if a correction is needed."),

        ("Who can see which tools?",
         "Admins and Management can see all tools across all sites. "
         "Data Entry users can only see tools at their assigned site. "
         "Inspectors, Store Managers, and Workers can look up any tool by scanning its QR code."),

        ("How do I export a tool's certificate?",
         "Go to Reports, find the tool, and click its row. "
         "You can view and print the tool certificate as a PDF from the tool's detail view."),
    ]

    for i, (q, a) in enumerate(faqs):
        story.append(Paragraph(f"Q{i+1}:  {q}", styles["faq_q"]))
        story.append(Paragraph(f"A:  {a}", styles["faq_a"]))
        story.append(sp(4))
        story.append(HRFlowable(width="100%", thickness=0.5, color=FLOW_BORDER))
        story.append(sp(2))

    story.append(sp(16))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT))
    story.append(sp(8))
    story.append(Paragraph(
        "For technical support or to report a system issue, contact your system administrator.",
        ParagraphStyle("footer_note", parent=styles["body"],
                       alignment=TA_CENTER, textColor=colors.grey, fontSize=9)
    ))
    story.append(Paragraph(
        "QR Code Tools Management System — User Guide v1.0 — May 2026",
        ParagraphStyle("footer_ver", parent=styles["body"],
                       alignment=TA_CENTER, textColor=ACCENT, fontSize=8,
                       fontName="Helvetica-Bold")
    ))

    # ── Build ─────────────────────────────────────────────────────────────────
    doc.build(
        story,
        onFirstPage=make_cover,
        onLaterPages=make_header_footer,
    )
    print(f"PDF created: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
