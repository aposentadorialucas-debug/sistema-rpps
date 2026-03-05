from datetime import date

def calcular_idade(data_nascimento):
    hoje = date.today()
    return hoje.year - data_nascimento.year

def regra_professor(cliente):
    idade = calcular_idade(cliente.data_nascimento)

    if cliente.sexo == 'F':
        idade_minima = 60
        tempo_minimo = 30
    else:
        idade_minima = 65
        tempo_minimo = 35

    return idade >= idade_minima