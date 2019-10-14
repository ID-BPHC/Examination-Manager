from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import TableStyle
from reportlab.lib.colors import black, Color


def get_title_style():
    style_sheet = getSampleStyleSheet()
    title_style = style_sheet["Title"]
    title_style.fontSize = 14
    return title_style


def get_semester_style():
    style_sheet = getSampleStyleSheet()
    semester_style = style_sheet["Title"]
    semester_style.fontSize = 11
    return semester_style


def get_date_style():
    style_sheet = getSampleStyleSheet()
    date_style = style_sheet["BodyText"]
    date_style.fontSize = 10
    date_style.alignment = 2
    return date_style


def get_greeting_style():
    style_sheet = getSampleStyleSheet()
    greeting_style = style_sheet["Heading3"]
    greeting_style.fontName = "Helvetica-Bold"
    greeting_style.fontSize = 10
    return greeting_style


def get_intro_style():
    style_sheet = getSampleStyleSheet()
    intro_style = style_sheet["BodyText"]
    return intro_style


def get_table_style():
    return TableStyle([
        ('BOX', (0,0), (-1,-1), 0.25, black),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, black),
        ('FONTNAME', (0, 0), (-1, 0), "Helvetica-Bold"),
    ])

def get_signature_style():
    style_sheet = getSampleStyleSheet()
    signature_style = style_sheet["Title"]
    signature_style.fontSize = 11
    signature_style.alignment = 2
    signature_style.leading = 10
    return signature_style
