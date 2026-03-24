def regra_idade_progressiva(servidor, tempos):

    from datetime import date

    idade = tempos.get("idade", 0)
    contribuicao = tempos.get("contribuicao", 0)

    ano = date.today().year

    if servidor.sexo == "M":

        idade_base = 61
        idade_limite = 65
        contribuicao_min = 35

    else:

        idade_base = 56
        idade_limite = 62
        contribuicao_min = 30

    incremento = (ano - 2019) * 0.5

    idade_minima = min(idade_limite, idade_base + incremento)

    requisitos = [

        {
            "descricao": f"Idade mínima ({idade_minima})",
            "cumprido": idade >= idade_minima,
            "faltante": max(0, idade_minima - idade)
        },

        {
            "descricao": f"Tempo contribuição ({contribuicao_min})",
            "cumprido": contribuicao >= contribuicao_min,
            "faltante": max(0, contribuicao_min - contribuicao)
        }

    ]

    return {

        "nome": "Idade Progressiva EC 103/2019",

        "apto": all(r["cumprido"] for r in requisitos),

        "integralidade": False,

        "paridade": False,

        "fundamento": "Art. 4º §1º EC 103/2019",

        "requisitos": requisitos

    }