from django.db import models

class Cliente(models.Model):

    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )

    CARGO_CHOICES = (
        ('servidor', 'Servidor Público'),
        ('professor', 'Professor'),
        ('militar', 'Policial/Bombeiro'),
    )

    nome = models.CharField(max_length=200)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)

    senha_gov = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Senha de acesso ao GOV.BR (uso interno do escritório)"
    )

    data_ingresso_servico_publico = models.DateField(null=True, blank=True)
    data_ingresso_cargo = models.DateField(null=True, blank=True)

    cargo_atual = models.CharField(max_length=20, choices=CARGO_CHOICES)

    tempo_atividade_especial = models.IntegerField(default=0)
    tempo_carreira = models.IntegerField(default=0)
    tempo_cargo = models.IntegerField(default=0)

    invalidez = models.BooleanField(default=False)

    def __str__(self):
        return self.nome