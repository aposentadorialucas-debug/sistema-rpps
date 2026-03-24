from .utils import calcular_idade, verificar_regra


def regra_permanente_servidor(cliente):

    idade = calcular_idade(cliente.data_nascimento)

    requisitos = [

        ("Idade mínima 65 (homem) / 62 (mulher)",
         idade >= 65 if cliente.sexo == "M" else idade >= 62),

        ("25 anos de contribuição",
         cliente.tempo_carreira >= 25),

        ("10 anos de serviço público",
         cliente.tempo_carreira >= 10),

        ("5 anos no cargo",
         cliente.tempo_cargo >= 5),
    ]

    return verificar_regra(requisitos)



def regra_transicao_pontos(cliente):

    idade = calcular_idade(cliente.data_nascimento)

    pontos = idade + cliente.tempo_carreira

    requisitos = [

        ("30 anos contribuição mulher / 35 homem",
         cliente.tempo_carreira >= 35 if cliente.sexo == "M" else cliente.tempo_carreira >= 30),

        ("20 anos serviço público",
         cliente.tempo_carreira >= 20),

        ("5 anos no cargo",
         cliente.tempo_cargo >= 5),

        ("Pontuação mínima",
         pontos >= 100 if cliente.sexo == "M" else pontos >= 90)
    ]

    return verificar_regra(requisitos)