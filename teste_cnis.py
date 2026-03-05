import pdfplumber
import re

def extrair_texto_cnis(caminho_pdf):
    texto_completo = ""

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_completo += texto + "\n"

    return texto_completo
def extrair_remuneracoes(texto):
    padrao = r'(\d{2}/\d{4})\s+([\d\.,]+)'
    resultados = re.findall(padrao, texto)

    remuneracoes = []

    for competencia, valor in resultados:
        valor_formatado = float(valor.replace('.', '').replace(',', '.'))
        remuneracoes.append({
            "competencia": competencia,
            "valor": valor_formatado
        })

    return remuneracoes
def extrair_indicadores(texto):
    indicadores = []

    if "PRPPS" in texto:
        indicadores.append("PRPPS")

    if "PSC-MEN-SM-EC103" in texto:
        indicadores.append("PSC-MEN-SM-EC103")

    if "IVIN-JORN-DIFERENCIADA" in texto:
        indicadores.append("IVIN-JORN-DIFERENCIADA")

    return indicadores
def extrair_indicadores(texto):
    indicadores = []

    if "PRPPS" in texto:
        indicadores.append("PRPPS")

    if "PSC-MEN-SM-EC103" in texto:
        indicadores.append("PSC-MEN-SM-EC103")

    if "IVIN-JORN-DIFERENCIADA" in texto:
        indicadores.append("IVIN-JORN-DIFERENCIADA")

    return indicadores