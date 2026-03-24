from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {

            'data_nascimento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),

            'data_ingresso_servico_publico': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),

            'data_ingresso_cargo': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),

            'data_ingresso_carreira': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),

            'telefone': forms.TextInput(attrs={
                'class': 'telefone',
                'placeholder': '(00) 00000-0000'
            }),

            'cep': forms.TextInput(attrs={
                'class': 'cep',
                'placeholder': '00000-000'
            }),
        }

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')

        if telefone:
            numeros = ''.join(filter(str.isdigit, telefone))

            if len(numeros) == 11:
                telefone = f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}"
            elif len(numeros) == 10:
                telefone = f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"

        return telefone


    def clean_cep(self):
        cep = self.cleaned_data.get('cep')

        if cep:
            numeros = ''.join(filter(str.isdigit, cep))

            if len(numeros) == 8:
                cep = f"{numeros[:5]}-{numeros[5:]}"

        return cep