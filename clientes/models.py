from django.db import models


class Cliente(models.Model):

    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )

    ESTADO_CIVIL = (
        ('solteiro', 'Solteiro(a)'),
        ('casado', 'Casado(a)'),
        ('divorciado', 'Divorciado(a)'),
        ('viuvo', 'Viúvo(a)'),
        ('uniao', 'União Estável'),
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

    ORGAO_RESPONSAVEL = (
        ('SECRETARIA MUNICIPAL DE LIMEIRA E SPPREV', 'SECRETARIA MUNICIPAL DE LIMEIRA E SPPREV'),
        ('IPRC E SPPREV', 'IPRC E SPPREV'),
        ('SECRETARIA MUNICIAL DE PIRACICABA E SPPREV', 'SECRETARIA MUNICIAL DE PIRACICABA E SPPREV'),
        ('ECRETARIA MUNICIAL DE SÃO CARLOS E SPPREV', 'SECRETARIA MUNICIAL DE SÃO CARLOS E SPPREV'),
        ('SECRETARIA MUNICIAL DE PIRASSUNINGA E SPPREV', 'SECRETARIA MUNICIAL DE PIRASSUNINGA E SPPREV'),
        ('SECRETARIA MUNICIAL DE SUMARE E SPPREV', 'SECRETARIA MUNICIAL DE SUMARE E SPPREV'),
        ('SECRETARIA MUNICIAL DE SÃO PAULO E SPPREV', 'SECRETARIA MUNICIAL DE SÃO PAULO E SPPREV'),
        ('SECRETARIA MUNICIAL DE AMERICANA E SPPREV', 'SECRETARIA MUNICIAL DE AMERICANA E SPPREV'),
        ('SECRETARIA MUNICIAL DE ARARAQUARA E SPPREV', 'SECRETARIA MUNICIAL DE ARARAQUARA E SPPREV'),
        ('SECRETARIA MUNICIAL DE CAMPINAS E SPPREV', 'SECRETARIA MUNICIAL DE CAMPINAS E SPPREV'),
        ('SECRETARIA MUNICIAL DE CAPIVARI E SPPREV', 'SECRETARIA MUNICIAL DE CAPIVARI E SPPREV'),
        ('SECRETARIA MUNICIAL DE SÃO JAU E SPPREV', 'SECRETARIA MUNICIAL DE SÃO JAU E SPPREV'),
        ('secretaria municipal de mogi mirim', 'SECRETARIA MUNICIAL DE MOGI MIRIM E SPPREV'),
        ('SECRETARIA DE SEGURANÇA PUBLICA DO ESTADO - POLICIA CIVIL', 'SECRETARIA DE SEGURANÇA PUBLICA DO ESTADO - POLICIA CIVIL'),
        ('SECRETARIA DE SEGURANÇA PUBLICA DO ESTADO - POLICIA MILITAR', 'SECRETARIA DE SEGURANÇA PUBLICA DO ESTADO - POLICIA MILITAR'),   
        ('SECRETARIA DE SEGURANÇA PUBLICA DO ESTADO - BOMBEIRO MILITAR', 'SECRETARIA DE SEGURANÇA PUBLICA DO ESTADO - BOMBEIRO MILITAR'),     
    
    )

    # ============================
    # DADOS PESSOAIS
    # ============================

    nome = models.CharField(max_length=200)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    estado_civil = models.CharField(
        max_length=20,
        choices=ESTADO_CIVIL,
        blank=True,
        null=True
    )

    data_nascimento = models.DateField()

    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)

    nacionalidade = models.CharField(max_length=50, default="Brasileiro", blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    endereco = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)

    # NOVO CAMPO
    orgao_responsavel = models.CharField(
        max_length=200,
        choices=ORGAO_RESPONSAVEL,
        blank=True,
        null=True,
    
    )

    # ============================
    # DADOS GOV
    # ============================

    senha_gov = models.CharField(max_length=100, blank=True, null=True)

    # ============================
    # DADOS FUNCIONAIS
    # ============================

    cargo_atual = models.CharField(max_length=20, choices=CARGO_CHOICES)

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
    # SITUAÇÕES
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

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.cpf})"