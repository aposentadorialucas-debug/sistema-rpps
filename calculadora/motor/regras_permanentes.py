def regra_idade_constitucional(servidor, tempos):

    idade = tempos.get("idade", 0)
    servico_publico = tempos.get("servico_publico", 0)
    cargo = tempos.get("cargo", 0)

    if servidor.sexo == "M":
        idade_min = 65
    else:
        idade_min = 60

    requisitos = [

        {
            "descricao": f"Idade mínima ({idade_min})",
            "cumprido": idade >= idade_min,
            "faltante": max(0, idade_min - idade)
        },

        {
            "descricao": "10 anos de serviço público",
            "cumprido": servico_publico >= 10,
            "faltante": max(0, 10 - servico_publico)
        },

        {
            "descricao": "5 anos no cargo",
            "cumprido": cargo >= 5,
            "faltante": max(0, 5 - cargo)
        }

    ]

    return {

        "nome": "Aposentadoria por idade – EC 20/1998",

        "apto": all(r["cumprido"] for r in requisitos),

        "integralidade": False,

        "paridade": False,

        "fundamento": "Art. 40 §1º III b CF (EC 20/1998)",

        "requisitos": requisitos

    }


def regras_permanentes(servidor, tempos):

    regras = []

    regras.append(
        regra_idade_constitucional(servidor, tempos)
    )

    return regras