def regras_deficiencia(servidor, tempos):

    regras = []

    if not servidor.deficiencia:
        return regras

    contribuicao = tempos["contribuicao"]

    requisitos = [

        {"descricao": "Servidor com deficiência",
         "cumprido": True},

        {"descricao": "Tempo mínimo 25 anos",
         "cumprido": contribuicao >= 25}

    ]

    regras.append({

        "nome": "Aposentadoria da Pessoa com Deficiência",

        "apto": all(r["cumprido"] for r in requisitos),

        "integralidade": False,
        "paridade": False,

        "fundamento": "LC 142/2013",

        "requisitos": requisitos

    })

    return regras