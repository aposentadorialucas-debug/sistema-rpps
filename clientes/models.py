from django.db import models


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

    # ============================
    # DADOS PESSOAIS
    # ============================

    nome = models.CharField(
        max_length=200,
        verbose_name="Nome completo"
    )

    sexo = models.CharField(
        max_length=1,
        choices=SEXO_CHOICES
    )

    data_nascimento = models.DateField()

    cpf = models.CharField(
        max_length=14,
        unique=True,
        blank=True,
        null=True
    )

    rg = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    endereco = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    # ============================
    # DADOS DE ACESSO GOV
    # (uso interno do escritório)
    # ============================

    senha_gov = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Senha de acesso ao GOV.BR (uso interno do escritório)"
    )

    # ============================
    # DADOS FUNCIONAIS
    # ============================

    cargo_atual = models.CharField(
        max_length=20,
        choices=CARGO_CHOICES,
        verbose_name="Cargo"
    )

    data_ingresso_servico_publico = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ingresso no serviço público"
    )

    data_ingresso_cargo = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ingresso no cargo atual"
    )

    # ============================
    # TEMPOS PREVIDENCIÁRIOS
    # ============================

    tempo_atividade_especial = models.IntegerField(
        default=0,
        help_text="Tempo especial em dias"
    )

    tempo_carreira = models.IntegerField(
        default=0,
        help_text="Tempo total na carreira (dias)"
    )

    tempo_cargo = models.IntegerField(
        default=0,
        help_text="Tempo no cargo atual (dias)"
    )

    # ============================
    # SITUAÇÕES ESPECIAIS
    # ============================

    invalidez = models.BooleanField(
        default=False,
        verbose_name="Possui invalidez?"
    )

    # ============================
    # CONTROLE DO SISTEMA
    # ============================

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    # ============================
    # REPRESENTAÇÃO
    # ============================

    def __str__(self):
        return f"{self.nome} ({self.cpf})"