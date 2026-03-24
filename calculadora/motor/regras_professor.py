from datetime import date

def regras_professor(servidor, tempos):

    regras = []

    idade = tempos.get("idade", 0)
    contribuicao = tempos.get("contribuicao", 0)
    servico_publico = tempos.get("servico_publico", 0)
    carreira = tempos.get("carreira", 0)
    cargo = tempos.get("cargo", 0)

    sexo = servidor.sexo

    # ==========================
    # REGRA EC 103/2019 PROFESSOR
    # ==========================

    if sexo == "M":
        idade_min = 60
        contrib_min = 30
    else:
        idade_min = 57
        contrib_min = 25

    if idade >= idade_min and contribuicao >= contrib_min:

        regras.append({
            "nome": "Professor - Regra Permanente EC 103/2019",
            "base_legal": "Art. 40 §5º CF + EC 103/2019",
            "integralidade": False,
            "paridade": False,
            "idade_minima": idade_min,
            "contribuicao_minima": contrib_min
        })

    return regras