from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm


def lista_clientes(request):

    busca = request.GET.get('q')

    if busca:
        clientes = Cliente.objects.filter(
            nome__icontains=busca
        ).order_by('nome')
    else:
        clientes = Cliente.objects.all().order_by('nome')

    return render(request, 'clientes/listar.html', {
        'clientes': clientes
    })


def cadastro_cliente(request):

    if request.method == 'POST':
        form = ClienteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('clientes:lista')

    else:
        form = ClienteForm()

    return render(request, 'clientes/cadastro.html', {
        'form': form
    })


def editar_cliente(request, cliente_id):

    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)

        if form.is_valid():
            form.save()
            return redirect('clientes:lista')

    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/cadastro.html', {
        'form': form
    })