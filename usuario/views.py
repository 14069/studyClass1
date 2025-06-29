from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib import messages
from socialapp.models import Postagem, Perfil
from .forms import UsuarioForm, EditarPerfilForm

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
    
    # Busca todos os perfis para exibir as fotos
    perfis = Perfil.objects.select_related('user').all()
    
    context = {
        'user': user,
        'user_profile': user_profile,
        'is_own_profile': is_own_profile,
        'posts': posts,
        'perfis': perfis,
    }
    
    return render(request, 'usuario/perfil_usuario.html', context)

@login_required
def editar_perfil(request):
    """
    View para editar o perfil do usuário logado.
    """
    # Obtém o perfil do usuário atual ou cria um novo se não existir
    try:
        perfil = Perfil.objects.get(matricula_perfil=request.user.username)
    except Perfil.DoesNotExist:
        perfil = Perfil.objects.create(
            matricula_perfil=request.user.username,
            nome_perfil=request.user.get_full_name() or request.user.username
        )
    
    if request.method == 'POST':
        # Cria uma instância do formulário com os dados do request e do perfil
        form = EditarPerfilForm(
            request.POST, 
            request.FILES, 
            instance=request.user,
            initial={
                'numero_telefone': perfil.numero_telefone,
                'data_nascimento': perfil.data_nascimento,
            }
        )
        
        if form.is_valid():
            # Atualiza os dados do usuário
            user = form.save(commit=False)
            
            # Se uma nova senha foi fornecida, atualiza a senha
            nova_senha = form.cleaned_data.get('nova_senha1')
            if nova_senha:
                user.set_password(nova_senha)
                update_session_auth_hash(request, user)  # Mantém o usuário logado
            
            user.save()
            
            # Atualiza os dados do perfil
            perfil.nome_perfil = form.cleaned_data.get('last_name', user.username)
            perfil.numero_telefone = form.cleaned_data.get('numero_telefone')
            perfil.data_nascimento = form.cleaned_data.get('data_nascimento')
            
            # Atualiza a foto de perfil se uma nova foi fornecida
            if 'foto_perfil' in request.FILES:
                perfil.foto_perfil = request.FILES['foto_perfil']
            
            perfil.save()
            
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil_usuario')
    else:
        # Cria uma instância do formulário com os dados atuais do usuário e perfil
        form = EditarPerfilForm(
            instance=request.user,
            initial={
                'numero_telefone': perfil.numero_telefone,
                'data_nascimento': perfil.data_nascimento,
            }
        )
    
    return render(request, 'usuario/editar_perfil.html', {
        'form': form,
        'perfil': perfil
    })
