from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):

    data_nascimento = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )

    data_ingresso_servico_publico = forms.DateField(
        required=False,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )

    data_ingresso_cargo = forms.DateField(
        required=False,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )

    class Meta:
        model = Cliente
        fields = '__all__'