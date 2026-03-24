def regras_bombeiro(servidor, tempos):

    regras = []

    if servidor.cargo_atual != "militar":
        return regras

    requisitos = [

        {
            "descricao": "Servidor militar estadual",
            "cumprido": servidor.cargo_atual == "militar"
        },

        {
            "descricao": "30 anos de serviço",
            "cumprido": tempo >= 30
        }

    ]

    regras.append({

        "nome": "Lei 13.954/2019 - Inatividade Militar",

        "apto": all(r["cumprido"] for r in requisitos),

        "integralidade": True,

        "paridade": True,

        "requisitos": requisitos

    })

    return regras