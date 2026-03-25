from io import BytesIO
from datetime import datetime
import re

from django.template.loader import render_to_string

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY


def limpar_html_para_reportlab(html):
    """
    Remove tags não suportadas pelo ReportLab
    """

    # Corrigir <br>
    html = html.replace("<br>", "<br/>")
    html = html.replace("<br />", "<br/>")

    # Remover DOCTYPE
    html = re.sub(r"<!DOCTYPE.*?>", "", html, flags=re.IGNORECASE)

    # Remover tags estruturais
    html = re.sub(r"</?(html|head|body|style|meta|link).*?>", "", html, flags=re.IGNORECASE)

    # Remover divs
    html = re.sub(r"</?div.*?>", "", html, flags=re.IGNORECASE)

    # Remover quebras duplicadas
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

    # LIMPAR HTML
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
        leading=16,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    )

    story = []

    story.append(Paragraph(html, estilo_contrato))
    story.append(Spacer(1, 12))

    doc.build(story)

    buffer.seek(0)
    return buffer