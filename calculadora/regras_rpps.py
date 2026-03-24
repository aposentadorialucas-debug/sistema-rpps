from .utils_calculo import montar_regra


def regras_rpps(cliente, idade, contribuicao):

    sexo = cliente.sexo

    regras = []

    # =====================================================
    # ART 40 ORIGINAL
    # =====================================================

    idade_min = 60 if sexo == "M" else 55
    tempo_min = 35 if sexo == "M" else 30

    requisitos = [

        {"descricao": "Idade mínima", "cumprido": idade >= idade_min},

        {"descricao": "Tempo contribuição", "cumprido": contribuicao >= tempo_min}

    ]

    dias_para = max(0, idade_min - idade) * 365

    regras.append(

        montar_regra(
            "Art. 40 CF (Direito adquirido)",
            requisitos,
            dias_para,
            True,
            True
        )

    )

    # =====================================================
    # EC 20
    # =====================================================

    idade_min = 53 if sexo == "M" else 48

    requisitos = [

        {"descricao": "Idade mínima EC20", "cumprido": idade >= idade_min},

        {"descricao": "Tempo contribuição",
         "cumprido": contribuicao >= (35 if sexo == "M" else 30)}

    ]

    dias_para = max(0, idade_min - idade) * 365

    regras.append(

        montar_regra(
            "EC 20/1998",
            requisitos,
            dias_para,
            True,
            True
        )

    )

    # =====================================================
    # EC 41
    # =====================================================

    idade_min = 60 if sexo == "M" else 55

    requisitos = [

        {"descricao": "Idade mínima", "cumprido": idade >= idade_min},

        {"descricao": "Tempo contribuição",
         "cumprido": contribuicao >= (35 if sexo == "M" else 30)},

        {"descricao": "10 anos serviço público",
         "cumprido": contribuicao >= 10},

        {"descricao": "5 anos cargo",
         "cumprido": cliente.tempo_cargo >= 5}

    ]

    dias_para = max(0, idade_min - idade) * 365

    regras.append(

        montar_regra(
            "EC 41/2003",
            requisitos,
            dias_para
        )

    )

    # =====================================================
    # EC 47
    # =====================================================

    requisitos = [

        {"descricao": "Tempo contribuição",
         "cumprido": contribuicao >= (35 if sexo == "M" else 30)},

        {"descricao": "25 anos serviço público",
         "cumprido": contribuicao >= 25},

        {"descricao": "15 anos carreira",
         "cumprido": contribuicao >= 15},

        {"descricao": "5 anos cargo",
         "cumprido": cliente.tempo_cargo >= 5}

    ]

    dias_para = 0

    regras.append(

        montar_regra(
            "EC 47/2005",
            requisitos,
            dias_para,
            True,
            True
        )

    )

    # =====================================================
    # EC 103 PERMANENTE
    # =====================================================

    idade_min = 65 if sexo == "M" else 62

    requisitos = [

        {"descricao": "Idade mínima", "cumprido": idade >= idade_min},

        {"descricao": "25 anos contribuição",
         "cumprido": contribuicao >= 25},

        {"descricao": "10 anos serviço público",
         "cumprido": contribuicao >= 10},

        {"descricao": "5 anos cargo",
         "cumprido": cliente.tempo_cargo >= 5}

    ]

    dias_para = max(0, idade_min - idade) * 365

    regras.append(

        montar_regra(
            "EC 103/2019 Permanente",
            requisitos,
            dias_para
        )

    )

    # =====================================================
    # TRANSIÇÃO PONTOS
    # =====================================================

    pontos = idade + contribuicao

    pontos_min = 100 if sexo == "M" else 90

    requisitos = [

        {"descricao": "30/35 contribuição",
         "cumprido": contribuicao >= (35 if sexo == "M" else 30)},

        {"descricao": "20 anos serviço público",
         "cumprido": contribuicao >= 20},

        {"descricao": "5 anos cargo",
         "cumprido": cliente.tempo_cargo >= 5},

        {"descricao": f"{pontos_min} pontos",
         "cumprido": pontos >= pontos_min}

    ]

    dias_para = max(0, pontos_min - pontos) * 365

    regras.append(

        montar_regra(
            "EC 103 Transição Pontos",
            requisitos,
            dias_para
        )

    )

    # =====================================================
    # COMPULSÓRIA
    # =====================================================

    requisitos = [

        {"descricao": "75 anos idade", "cumprido": idade >= 75}

    ]

    dias_para = max(0, 75 - idade) * 365

    regras.append(

        montar_regra(
            "EC 88/2015 Compulsória",
            requisitos,
            dias_para
        )

    )

    return regras