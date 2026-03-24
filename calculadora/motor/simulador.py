def anos_faltantes(atual, minimo):

    if atual >= minimo:
        return 0

    return round(minimo - atual, 2)