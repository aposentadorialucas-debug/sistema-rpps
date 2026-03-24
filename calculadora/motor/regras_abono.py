def regras_abono(servidor, tempos):

    regras = []

    idade = tempos.get("idade", 0)
    contribuicao = tempos.get("contribuicao", 0)

    idade_min = 65 if servidor.sexo == "M" else 62

    requisitos = [

        {
            "descricao": f"Idade mínima ({idade_min})",
            "cumprido": idade >= idade_min
        },

        {
            "descricao": "Tempo mínimo contribuição (25)",
            "cumprido": contribuicao >= 25
        }

    ]

    if all(r["cumprido"] for r in requisitos):

        regras.append({

            "nome": "Abono Permanência",

            "apto": True,

            "integralidade": False,
            "paridade": False,

            "fundamento": "Art. 40 §19 CF",

            "requisitos": requisitos

        })

    return regras