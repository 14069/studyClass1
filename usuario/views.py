from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import UsuarioForm


# Create your views here.
def new_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            return redirect('login')
    else:
        form = UsuarioForm()
    return render(request, 'usuario/usuario.html', {'form': form})
