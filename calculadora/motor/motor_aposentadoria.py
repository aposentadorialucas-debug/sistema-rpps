from .calculos import calcular_tempos
from .tempos_padrao import tempos_padrao

from .regras_servidor import regras_servidor
from .regras_professor import regras_professor
from .regras_policial import regras_policial
from .regras_bombeiro import regras_bombeiro

from .regras_transicao import regras_transicao
from .regras_permanentes import regras_permanentes

from .regras_deficiencia import regras_deficiencia
from .regras_direito_adquirido import regras_direito_adquirido
from .regras_abono import regras_abono
from .regras_invalidez import regras_invalidez


def analisar_aposentadoria(servidor):

    regras = []

    tempos_calculados = calcular_tempos(servidor)

    tempos = tempos_padrao()
    tempos.update(tempos_calculados)

    # regras base
    regras += regras_servidor(servidor, tempos)

    # permanentes
    regras += regras_permanentes(servidor, tempos)

    # carreiras
    regras += regras_professor(servidor, tempos)
    regras += regras_policial(servidor, tempos)
    regras += regras_bombeiro(servidor, tempos)

    # transição
    regras += regras_transicao(servidor, tempos)

    # especiais
    regras += regras_deficiencia(servidor, tempos)
    regras += regras_invalidez(servidor, tempos)

    # direito adquirido
    regras += regras_direito_adquirido(servidor, tempos)

    # abono
    regras += regras_abono(servidor, tempos)

    return regras