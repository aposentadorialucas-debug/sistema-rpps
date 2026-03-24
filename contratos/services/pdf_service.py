from io import BytesIO
from datetime import datetime

from django.template.loader import render_to_string

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm


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

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(html, styles['Normal']))
    story.append(Spacer(1, 12))

    doc.build(story)

    buffer.seek(0)
    return buffer