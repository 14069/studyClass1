from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from socialapp.models import Postagem, Perfil  # Importando o modelo Perfil
from .forms import UsuarioForm

User = get_user_model()

def new_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UsuarioForm()
    return render(request, 'usuario/new_usuario.html', {'form': form})

@login_required
def perfil_usuario(request, username=None):
    # Se nenhum username for fornecido, mostra o próprio perfil
    if username is None:
        user = request.user
        is_own_profile = True
    else:
        user = get_object_or_404(User, username=username)
        is_own_profile = (request.user == user)
    
    # Busca o perfil do usuário
    try:
        user_profile = Perfil.objects.get(matricula_perfil=user.username)
    except Perfil.DoesNotExist:
        user_profile = None
    
    # Busca as postagens do usuário
    posts = Postagem.objects.filter(autor_postagem=user).order_by('-data_postagem')
    
    context = {
        'user': user,
        'user_profile': user_profile,
        'is_own_profile': is_own_profile,
        'posts': posts,
    }
    
    return render(request, 'usuario/perfil_usuario.html', context)
