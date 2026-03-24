def regra_ec41(servidor, tempos):

    idade = tempos.get("idade", 0)
    contribuicao = tempos.get("contribuicao", 0)
    servico_publico = tempos.get("servico_publico", 0)
    cargo = tempos.get("cargo", 0)

    if servidor.sexo == "M":

        idade_min = 60
        contribuicao_min = 35

    else:

        idade_min = 55
        contribuicao_min = 30

    requisitos = [

        {
            "descricao": f"Idade mínima ({idade_min})",
            "cumprido": idade >= idade_min,
            "faltante": max(0, idade_min - idade)
        },

        {
            "descricao": f"Tempo de contribuição ({contribuicao_min})",
            "cumprido": contribuicao >= contribuicao_min,
            "faltante": max(0, contribuicao_min - contribuicao)
        },

        {
            "descricao": "20 anos de serviço público",
            "cumprido": servico_publico >= 20,
            "faltante": max(0, 20 - servico_publico)
        },

        {
            "descricao": "5 anos no cargo",
            "cumprido": cargo >= 5,
            "faltante": max(0, 5 - cargo)
        }

    ]

    return {

        "nome": "Direito adquirido – EC 41/2003",

        "apto": all(r["cumprido"] for r in requisitos),

        "integralidade": True,

        "paridade": True,

        "fundamento": "Art. 6º EC 41/2003",

        "requisitos": requisitos

    }


def regra_ec47(servidor, tempos):

    idade = tempos.get("idade", 0)
    contribuicao = tempos.get("contribuicao", 0)

    pontos = idade + contribuicao

    if servidor.sexo == "M":

        pontos_min = 95
        contribuicao_min = 35

    else:

        pontos_min = 85
        contribuicao_min = 30

    requisitos = [

        {
            "descricao": f"Pontuação mínima ({pontos_min})",
            "cumprido": pontos >= pontos_min,
            "faltante": max(0, pontos_min - pontos)
        },

        {
            "descricao": f"Tempo mínimo de contribuição ({contribuicao_min})",
            "cumprido": contribuicao >= contribuicao_min,
            "faltante": max(0, contribuicao_min - contribuicao)
        }

    ]

    return {

        "nome": "Direito adquirido – EC 47/2005",

        "apto": all(r["cumprido"] for r in requisitos),

        "integralidade": True,

        "paridade": True,

        "fundamento": "Art. 3º EC 47/2005",

        "requisitos": requisitos

    }


def regras_direito_adquirido(servidor, tempos):

    regras = []

    regras.append(regra_ec41(servidor, tempos))

    regras.append(regra_ec47(servidor, tempos))

    return regras