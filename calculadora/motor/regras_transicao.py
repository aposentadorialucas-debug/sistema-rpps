from datetime import date


def regra_pontos_ec103(servidor, tempos):

    idade = tempos.get("idade", 0)
    contribuicao = tempos.get("contribuicao", 0)

    pontos = idade + contribuicao
    ano = date.today().year

    if servidor.sexo == "M":
        base = 96
        limite = 105
        contribuicao_min = 35
    else:
        base = 86
        limite = 100
        contribuicao_min = 30

    incremento = max(0, ano - 2019)
    pontos_minimos = min(limite, base + incremento)

    requisitos = [
        {
            "descricao": f"Pontuação mínima ({pontos_minimos})",
            "cumprido": pontos >= pontos_minimos,
            "faltante": max(0, pontos_minimos - pontos)
        },
        {
            "descricao": f"Tempo de contribuição ({contribuicao_min})",
            "cumprido": contribuicao >= contribuicao_min,
            "faltante": max(0, contribuicao_min - contribuicao)
        }
    ]

    return {
        "nome": "EC 103 – Pontos",
        "apto": all(r["cumprido"] for r in requisitos),
        "integralidade": False,
        "paridade": False,
        "fundamento": "Art. 4º EC 103/2019",
        "requisitos": requisitos
    }


def regra_idade_progressiva_ec103(servidor, tempos):

    idade = tempos.get("idade", 0)
    contribuicao = tempos.get("contribuicao", 0)

    ano = date.today().year

    if servidor.sexo == "M":
        idade_base = 61
        contribuicao_min = 35
        idade_limite = 65
    else:
        idade_base = 56
        contribuicao_min = 30
        idade_limite = 62

    incremento = (ano - 2019) * 0.5
    idade_minima = min(idade_limite, idade_base + incremento)

    requisitos = [
        {
            "descricao": f"Idade mínima progressiva ({idade_minima:.1f})",
            "cumprido": idade >= idade_minima,
            "faltante": max(0, idade_minima - idade)
        },
        {
            "descricao": f"Tempo de contribuição ({contribuicao_min})",
            "cumprido": contribuicao >= contribuicao_min,
            "faltante": max(0, contribuicao_min - contribuicao)
        }
    ]

    return {
        "nome": "EC 103 – Idade Progressiva",
        "apto": all(r["cumprido"] for r in requisitos),
        "integralidade": False,
        "paridade": False,
        "fundamento": "Art. 4º §1º EC 103/2019",
        "requisitos": requisitos
    }


def regra_pedagio_100_ec103(servidor, tempos):

    idade = tempos.get("idade", 0)
    contribuicao = tempos.get("contribuicao", 0)

    if servidor.sexo == "M":
        idade_min = 60
        contribuicao_min = 35
    else:
        idade_min = 57
        contribuicao_min = 30

    requisitos = [
        {
            "descricao": f"Idade mínima ({idade_min})",
            "cumprido": idade >= idade_min,
            "faltante": max(0, idade_min - idade)
        },
        {
            "descricao": f"Tempo mínimo ({contribuicao_min})",
            "cumprido": contribuicao >= contribuicao_min,
            "faltante": max(0, contribuicao_min - contribuicao)
        },
        {
            "descricao": "Pedágio de 100% (tempo faltante em 13/11/2019)",
            "cumprido": False,
            "faltante": "A calcular"
        }
    ]

    integralidade = False
    paridade = False

    if hasattr(servidor, "data_ingresso"):
        if servidor.data_ingresso.year <= 2003:
            integralidade = True
            paridade = True

    return {
        "nome": "EC 103 – Pedágio 100%",
        "apto": idade >= idade_min and contribuicao >= contribuicao_min,
        "integralidade": integralidade,
        "paridade": paridade,
        "fundamento": "Art. 20 EC 103/2019",
        "requisitos": requisitos
    }


def regra_ec41_pedagio20(servidor, tempos):

    idade = tempos.get("idade", 0)
    contribuicao = tempos.get("contribuicao", 0)

    if servidor.sexo == "M":
        idade_min = 53
        contribuicao_min = 35
    else:
        idade_min = 48
        contribuicao_min = 30

    requisitos = [
        {
            "descricao": f"Idade mínima ({idade_min})",
            "cumprido": idade >= idade_min,
            "faltante": max(0, idade_min - idade)
        },
        {
            "descricao": f"Tempo mínimo ({contribuicao_min})",
            "cumprido": contribuicao >= contribuicao_min,
            "faltante": max(0, contribuicao_min - contribuicao)
        },
        {
            "descricao": "Pedágio de 20%",
            "cumprido": False,
            "faltante": "A calcular"
        }
    ]

    return {
        "nome": "EC 41 – Pedágio 20%",
        "apto": idade >= idade_min and contribuicao >= contribuicao_min,
        "integralidade": False,
        "paridade": False,
        "fundamento": "Art. 2º EC 41/2003",
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
            "descricao": f"Pontuação ({pontos_min})",
            "cumprido": pontos >= pontos_min,
            "faltante": max(0, pontos_min - pontos)
        },
        {
            "descricao": f"Tempo mínimo ({contribuicao_min})",
            "cumprido": contribuicao >= contribuicao_min,
            "faltante": max(0, contribuicao_min - contribuicao)
        }
    ]

    return {
        "nome": "EC 47 – 85/95",
        "apto": all(r["cumprido"] for r in requisitos),
        "integralidade": True,
        "paridade": True,
        "fundamento": "Art. 3º EC 47/2005",
        "requisitos": requisitos
    }


def regras_transicao(servidor, tempos):

    return [

        regra_pontos_ec103(servidor, tempos),

        regra_idade_progressiva_ec103(servidor, tempos),

        regra_pedagio_100_ec103(servidor, tempos),

        regra_ec41_pedagio20(servidor, tempos),

        regra_ec47(servidor, tempos),

    ]