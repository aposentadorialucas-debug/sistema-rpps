from django.db import models
from datetime import date


class Cliente(models.Model):

    # ============================
    # CONSTANTES
    # ============================

    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )

    CARGO_CHOICES = (
        ('servidor', 'Servidor Público'),
        ('professor', 'Professor'),
        ('militar', 'Policial / Bombeiro'),
    )

    GRAU_DEFICIENCIA = (
        ('leve', 'Leve'),
        ('moderada', 'Moderada'),
        ('grave', 'Grave'),
    )

    # ============================
    # DADOS PESSOAIS
    # ============================

    nome = models.CharField(max_length=200)

    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES
    )

    data_nascimento = models.DateField()

    cpf = models.CharField(
        max_length=14,
        unique=True,
        null=True,
        blank=True
    )

    rg = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    endereco = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    # ============================
    # FUNCIONAL
    # ============================

    cargo_atual = models.CharField(
        max_length=20,
        choices=CARGO_CHOICES
    )

    data_ingresso_servico_publico = models.DateField(null=True, blank=True)

    data_ingresso_cargo = models.DateField(null=True, blank=True)

    data_ingresso_carreira = models.DateField(null=True, blank=True)

    # ============================
    # TEMPOS
    # ============================

    tempo_contribuicao = models.IntegerField(default=0)

    tempo_servico_publico_dias = models.IntegerField(default=0)

    tempo_carreira = models.IntegerField(default=0)

    tempo_cargo = models.IntegerField(default=0)

    tempo_magisterio = models.IntegerField(default=0)

    tempo_atividade_policial = models.IntegerField(default=0)

    tempo_atividade_especial = models.IntegerField(default=0)

    # ============================
    # SITUAÇÕES ESPECIAIS
    # ============================

    invalidez = models.BooleanField(default=False)

    deficiencia = models.BooleanField(default=False)

    grau_deficiencia = models.CharField(
        max_length=10,
        choices=GRAU_DEFICIENCIA,
        null=True,
        blank=True
    )

    direito_adquirido = models.BooleanField(default=False)

    # ============================
    # CONTROLE
    # ============================

    criado_em = models.DateTimeField(auto_now_add=True)

    atualizado_em = models.DateTimeField(auto_now=True)

    # ============================
    # REPRESENTAÇÃO
    # ============================

    def __str__(self):
        return self.nome

    # ============================
    # PROPRIEDADES
    # ============================

    @property
    def idade(self):

        hoje = date.today()

        idade = hoje.year - self.data_nascimento.year

        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
            idade -= 1

        return idade

    @property
    def anos_contribuicao(self):
        return self.tempo_contribuicao / 365

    @property
    def anos_magisterio(self):
        return self.tempo_magisterio / 365

    @property
    def anos_atividade_policial(self):
        return self.tempo_atividade_policial / 365

    @property
    def anos_servico_publico(self):

        if not self.data_ingresso_servico_publico:
            return 0

        hoje = date.today()

        anos = hoje.year - self.data_ingresso_servico_publico.year

        if (hoje.month, hoje.day) < (
            self.data_ingresso_servico_publico.month,
            self.data_ingresso_servico_publico.day
        ):
            anos -= 1

        return anos

    @property
    def anos_cargo(self):

        if not self.data_ingresso_cargo:
            return 0

        hoje = date.today()

        anos = hoje.year - self.data_ingresso_cargo.year

        if (hoje.month, hoje.day) < (
            self.data_ingresso_cargo.month,
            self.data_ingresso_cargo.day
        ):
            anos -= 1

        return anos