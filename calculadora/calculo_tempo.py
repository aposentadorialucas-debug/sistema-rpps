from datetime import date

def calcular_tempo(data_inicio):
    """
    Calcula anos completos desde data_inicio até hoje.
    Retorna 0 se data_inicio for None.
    """
    if not data_inicio:
        return 0

    hoje = date.today()
    anos = hoje.year - data_inicio.year
    meses = hoje.month - data_inicio.month
    dias = hoje.day - data_inicio.day

    if dias < 0:
        meses -= 1
        dias += 30  # aproximação suficiente
    if meses < 0:
        anos -= 1
        meses += 12

    return anos

def calcular_tempos(servidor):
    """
    Retorna todos os tempos relevantes de um servidor em um dict padronizado.
    Chaves usadas por todas as regras para evitar KeyError.
    """
    tempos = {
        "idade": calcular_tempo(getattr(servidor, "data_nascimento", None)),
        "tempo_servico_publico": calcular_tempo(getattr(servidor, "data_ingresso_servico_publico", None)),
        "tempo_cargo": calcular_tempo(getattr(servidor, "data_ingresso_cargo", None)),
        "tempo_carreira": calcular_tempo(getattr(servidor, "data_ingresso_carreira", None)),
        "tempo_contribuicao": getattr(servidor, "tempo_contribuicao", 0),
        "tempo_magisterio": getattr(servidor, "tempo_magisterio", 0),
    }
    return tempos