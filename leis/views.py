from django.shortcuts import render

def lista_leis(request):
    return render(request, 'leis/lista.html')