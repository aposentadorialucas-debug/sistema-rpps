def regra_pedagio_100(servidor, tempos):

    idade = tempos["idade"]
    contribuicao = tempos["contribuicao"]

    sexo = servidor.sexo

    idade_min = 60 if sexo == "M" else 57
    contrib_min = 35 if sexo == "M" else 30

    pedagio = contrib_min - contribuicao

    requisitos = [

        {
            "descricao": f"Idade mínima ({idade_min})",
            "cumprido": idade >= idade_min,
            "faltante": max(0, idade_min - idade)
        },

        {
            "descricao": "Pedágio 100%",
            "cumprido": contribuicao >= contrib_min + pedagio,
            "faltante": max(0, (contrib_min + pedagio) - contribuicao)
        }

    ]

    return {

        "nome": "EC 103/2019 – Pedágio 100%",

        "apto": all(r["cumprido"] for r in requisitos),

        "integralidade": True,
        "paridade": False,

        "fundamento": "Art. 20 EC 103/2019",

        "requisitos": requisitos
    }