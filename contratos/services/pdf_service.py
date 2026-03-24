import os
from io import BytesIO
from datetime import datetime

from django.template.loader import get_template
from django.conf import settings

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.units import cm

from xhtml2pdf import pisa


def gerar_pdf_contrato(cliente, tipo):

    buffer = BytesIO()

    # Mapeamento dos templates
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

    template = get_template(template_path)

    contexto = {
        "cliente": cliente,
        "data_hoje": datetime.now().strftime("%d/%m/%Y"),
        "valor": "",
        "valor_fixo": "",
        "valor_planejamento": "",
        "percentual_exito": "10%",
    }

    html = template.render(contexto)

    pisa.CreatePDF(
        html,
        dest=buffer,
        encoding='UTF-8'
    )

    buffer.seek(0)

    return buffer