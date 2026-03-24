def regras_policial(servidor, tempos):

    regras = []

    if servidor.cargo_atual != "policial":
        return regras

    idade = tempos["idade"]
    tempo_policial = tempos["atividade_policial"]

    sexo = servidor.sexo

    idade_min = 55 if sexo == "M" else 52
    tempo_min = 30 if sexo == "M" else 25

    requisitos = [

        {
            "descricao": f"Idade mínima ({idade_min})",
            "cumprido": idade >= idade_min,
            "faltante": max(0, idade_min - idade)
        },

        {
            "descricao": f"Tempo atividade policial ({tempo_min})",
            "cumprido": tempo_policial >= tempo_min,
            "faltante": max(0, tempo_min - tempo_policial)
        }

    ]

    regras.append({

        "nome": "LC 51/1985 – Aposentadoria Policial",

        "apto": all(r["cumprido"] for r in requisitos),

        "integralidade": True,
        "paridade": True,

        "fundamento": "LC 51/1985 + EC 103/2019",

        "requisitos": requisitos
    })

    return regras