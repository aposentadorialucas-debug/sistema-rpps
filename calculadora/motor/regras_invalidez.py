def regras_invalidez(servidor, tempos):

    regras = []

    if servidor.invalidez:

        regra = {

            "nome": "Aposentadoria por Invalidez Permanente",

            "apto": True,

            "idade_faltante": 0,
            "tempo_faltante": 0,

            "integralidade": True,
            "paridade": False,

            "fundamento": "Art. 40 §1º I da Constituição Federal (EC 103/2019)"

        }

        regras.append(regra)

    return regras