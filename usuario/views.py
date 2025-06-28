from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import UsuarioForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def new_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            return redirect('login')
    else:
        form = UsuarioForm()
    return render(request, 'usuario/new_usuario.html', {'form': form})

@login_required
def perfil_usuario(request):
    return render(request, 'usuario/perfil_usuario.html')
