def regras_servidor(servidor, tempos):

    regras = []

    idade = tempos["idade"]
    contribuicao = tempos["contribuicao"]
    servico_publico = tempos["servico_publico"]
    cargo = tempos["cargo"]

    sexo = servidor.sexo

    idade_min = 65 if sexo == "M" else 62
    contribuicao_min = 25

    requisitos = [

        {
            "descricao": f"Idade mínima ({idade_min})",
            "cumprido": idade >= idade_min,
            "faltante": max(0, idade_min - idade)
        },

        {
            "descricao": "Tempo mínimo contribuição (25)",
            "cumprido": contribuicao >= contribuicao_min,
            "faltante": max(0, contribuicao_min - contribuicao)
        },

        {
            "descricao": "10 anos serviço público",
            "cumprido": servico_publico >= 10,
            "faltante": max(0, 10 - servico_publico)
        },

        {
            "descricao": "5 anos no cargo",
            "cumprido": cargo >= 5,
            "faltante": max(0, 5 - cargo)
        }

    ]

    regras.append({

        "nome": "Servidor Público – Regra Permanente EC 103/2019",

        "apto": all(r["cumprido"] for r in requisitos),

        "integralidade": False,

        "paridade": False,

        "fundamento": "Art. 40 §1º III CF – EC 103/2019",

        "requisitos": requisitos

    })

    return regras