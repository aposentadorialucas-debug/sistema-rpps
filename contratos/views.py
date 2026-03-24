from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from clientes.models import Cliente
from .services.pdf_service import gerar_pdf_contrato


def lista(request):
    clientes = Cliente.objects.all()
    return render(request, 'contratos/lista.html', {
        'clientes': clientes
    })


def tipos_contrato(request, cliente_id):

    cliente = get_object_or_404(Cliente, id=cliente_id)

    return render(request, 'contratos/tipos_contrato.html', {
        'cliente': cliente
    })


def gerar_contrato(request, cliente_id, tipo):

    cliente = get_object_or_404(Cliente, id=cliente_id)

    pdf = gerar_pdf_contrato(cliente, tipo)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="contrato_{cliente.nome}.pdf"'

    return response