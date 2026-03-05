from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm
from django.db.models import Q

@login_required

def listar_clientes(request):
    query = request.GET.get('q')
    clientes = Cliente.objects.all()

    if query:
        clientes = clientes.filter(
            Q(nome__icontains=query) |
            Q(cpf__icontains=query) |
            Q(rg__icontains=query) |
            Q(cargo_atual__icontains=query)
        )

    return render(request, 'clientes/listar.html', {
        'clientes': clientes
    })


def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()

    return render(request, 'clientes/cadastro.html', {'form': form})


def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('calcular_aposentadoria', id=cliente.id)
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/cadastro.html', {'form': form})


def excluir_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return redirect('listar_clientes')