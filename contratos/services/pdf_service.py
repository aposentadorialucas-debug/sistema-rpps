from io import BytesIO
from datetime import datetime
import re
import os

from django.template.loader import render_to_string
from django.conf import settings

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY


def limpar_html_para_reportlab(html):
    """
    Remove tags não suportadas pelo ReportLab
    """

    html = html.replace("<br>", "<br/>")
    html = html.replace("<br />", "<br/>")

    html = re.sub(r"<!DOCTYPE.*?>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"</?(html|head|body|style|meta|link).*?>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"</?div.*?>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"\n+", " ", html)

    return html


def gerar_pdf_contrato(cliente, tipo):

    buffer = BytesIO()

    templates = {
        "procuracao": "contratos/procuracao.html",
        "abono": "contratos/abono.html",
        "aposentadoria": "contratos/aposentadoria.html",
        "planejamento": "contratos/planejamento.html",
        "revisao": "contratos/revisao.html",
        "hipossuficiencia": "contratos/hipossuficiencia.html",
    }

    template_path = templates.get(tipo)

    if not template_path:
        raise ValueError("Tipo de contrato inválido")

    contexto = {
        "cliente": cliente,
        "data_hoje": datetime.now().strftime("%d/%m/%Y"),
        "valor": "",
        "valor_fixo": "",
        "valor_planejamento": "",
        "percentual_exito": "10%",
    }

    html = render_to_string(template_path, contexto)

    # Limpar HTML
    html = limpar_html_para_reportlab(html)

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2.5 * cm,
        leftMargin=3 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
    )

    styles = getSampleStyleSheet()

    estilo_contrato = ParagraphStyle(
        'Contrato',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=18,
        alignment=TA_JUSTIFY,
        firstLineIndent=20,
        spaceAfter=8,
    )

    story = []

    # LOGO
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'css', 'img', 'logo1.png')

    if os.path.exists(logo_path):
        logo = Image(logo_path, width=450, height=120)
        story.append(logo)
        story.append(Spacer(1, 12))

    # TEXTO
    story.append(Paragraph(html, estilo_contrato))
    story.append(Spacer(1, 12))

    doc.build(story)

    buffer.seek(0)
    return buffer