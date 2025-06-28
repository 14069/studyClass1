from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from socialapp.forms import AvaliaForms, PostagemForms, PerfilForms, TelefoneForms, PerfilPostForms, CommentForm
from socialapp.models import Avalia, Postagem, Perfil, Telefone, Perfil_post, Like, Comment
from django.http import JsonResponse, Http404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required
def index(request):
    # Mostra todas as postagens para todos os usuários
    posts = Postagem.objects.all().order_by('-data_postagem')
    
    # Obtém os IDs dos posts curtidos pelo usuário
    liked_post_ids = Like.objects.filter(user=request.user).values_list('postagem_id', flat=True)
    comment_form = CommentForm()

    return render(request, 'social/index.html', {
        'posts': posts,
        'liked_post_ids': list(liked_post_ids),  # Converte para lista para evitar múltiplas consultas no template
        'comment_form': comment_form,
        'is_superuser': request.user.is_superuser,
        'current_user': request.user.username
    })

@login_required
def my_posts(request):
    # Mostra apenas as postagens do usuário logado
    posts = Postagem.objects.filter(autor_postagem=request.user.username).order_by('-data_postagem')
    
    # Obtém os IDs dos posts curtidos pelo usuário
    liked_post_ids = Like.objects.filter(user=request.user).values_list('postagem_id', flat=True)
    comment_form = CommentForm()

    return render(request, 'social/my_posts.html', {
        'posts': posts,
        'liked_post_ids': list(liked_post_ids),
        'comment_form': comment_form,
        'is_superuser': request.user.is_superuser,
        'current_user': request.user.username
    })

@login_required
def perfil_usuario(request, username=None):
    # Se nenhum nome de usuário for fornecido, mostra o perfil do usuário logado
    if not username:
        username = request.user.username
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("Usuário não encontrado")
    
    # Tenta obter o perfil do usuário, se existir
    try:
        perfil = Perfil.objects.get(nome_perfil=username)
    except Perfil.DoesNotExist:
        perfil = None
    
    # Obtém as postagens do usuário
    posts = Postagem.objects.filter(autor_postagem=username).order_by('-data_postagem')[:5]
    
    # Verifica se o perfil sendo visualizado pertence ao usuário logado
    is_own_profile = (request.user.username == username)
    
    context = {
        'profile_user': user,
        'perfil': perfil,
        'posts': posts,
        'is_own_profile': is_own_profile,
    }
    
    return render(request, 'social/perfil_usuario.html', context)

@login_required
def editar_perfil(request):
    # Obtém o perfil do usuário atual ou cria um novo se não existir
    perfil, created = Perfil.objects.get_or_create(
        nome_perfil=request.user.username,
        defaults={
            'nome_perfil': request.user.username,
            'data_nascimento': None,
            'matricula_perfil': '',
        }
    )
    
    if request.method == 'POST':
        form = PerfilForms(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.nome_perfil = request.user.username  # Garante que o nome do perfil seja o nome de usuário
            perfil.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil_usuario')
    else:
        form = PerfilForms(instance=perfil)
    
    context = {
        'form': form,
        'perfil': perfil,
    }
    
    return render(request, 'social/editar_perfil.html', context)

def home(request):
    postagens = Postagem.objects.all().order_by('-data_postagem')[:5]
    return render(request, 'social/home.html', {'postagens': postagens})

def contato(request):
    return render(request, 'social/contact.html')

def sobre(request):
    return render(request, 'social/about.html')

#def postar(request):
    return render(request, 'social/post.html')

def new_avalia(request):
    avas = Avalia.objects.all()
    form = AvaliaForms()
    if request.method=='POST':
        form =AvaliaForms(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            obj.save()
            form= AvaliaForms()
    return render(request, 'social/new_avalia.html', {'form':form, 'avas':avas})

def editar_avalia(request, id):
    avaliado =get_object_or_404(Avalia, pk=id)
    form =AvaliaForms(instance=avaliado)
    avas =Avalia.objects.all()

    if(request.method =="POST"):
        form = AvaliaForms(request.POST, request.FILES, instance=avaliado)
        if form.is_valid():
            form.save()
            return redirect('new_avalia')
        return render(request, 'social/editar_avalia.html', {'form': form, 'avas': avas, 'avaliado':avaliado})
    else:
        return render(request, 'social/editar_avalia.html',{'form': form, 'avas': avas, 'avaliado': avaliado})



def deleta_avalia(request,id):
    avaliado = get_object_or_404(Avalia, pk=id)
    form = AvaliaForms(instance=avaliado)
    avas = Avalia.objects.all()
    if request.method == "POST":
        avaliado.delete()
        return redirect('new_avalia')
    return render(request,'social/deleta_avalia.html',{'avaliado':avaliado, 'form':form, 'avas':avas})

# Postagem
@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostagemForms(request.POST, request.FILES)
        if form.is_valid():
            postagem = form.save(commit=False)
            postagem.autor_postagem = request.user
            postagem.save()
            return redirect('my_posts')  # Redireciona para a lista de postagens do usuário
    else:
        form = PostagemForms()
    
    # Mostra apenas as postagens do usuário atual
    posts = Postagem.objects.filter(autor_postagem=request.user).order_by('-data_postagem')
    return render(request, 'social/new_post.html', {
        'form': form, 
        'posts': posts,
        'is_own_posts': True  # Indica que são as postagens do próprio usuário
    })


@login_required
def editar_post(request, id):
    post = get_object_or_404(Postagem, pk=id)
    
    # Permite que o autor ou um superusuário edite a postagem
    if str(post.autor_postagem) != str(request.user.username) and not request.user.is_superuser:
        return redirect('index')
        
    form = PostagemForms(instance=post)
    
    # Mostra apenas as postagens do usuário atual
    posts = Postagem.objects.filter(autor_postagem=request.user).order_by('-data_postagem')

    if request.method == "POST":
        form = PostagemForms(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('my_posts')  # Redireciona para a lista de postagens do usuário
        return render(request, 'social/editar_post.html', {
            'form': form, 
            'posts': posts, 
            'post': post,
            'is_own_posts': True  # Indica que são as postagens do próprio usuário
        })
    else:
        return render(request, 'social/editar_post.html', {
            'form': form, 
            'posts': posts, 
            'post': post,
            'is_own_posts': True  # Indica que são as postagens do próprio usuário
        })



@login_required
def deleta_post(request, id):
    post = get_object_or_404(Postagem, pk=id)
    
    # Permite que o autor ou um superusuário exclua a postagem
    if str(post.autor_postagem) != str(request.user.username) and not request.user.is_superuser:
        return redirect('index')

    if request.method == "POST":
        post.delete()
        return redirect('index')
    
    # Redireciona para o início se o método for GET para evitar exclusão acidental.
    return redirect('index')


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Postagem, id_postagem=post_id)
    like, created = Like.objects.get_or_create(user=request.user, postagem=post)

    if not created:
        # Se o like já existia, o usuário está descurtindo.
        like.delete()
        liked = False
    else:
        # Se o like foi criado agora, o usuário está curtindo.
        liked = True

    # Retorna a nova contagem de likes e o status atual do like do usuário
    return JsonResponse({
        'likes_count': post.likes.count(),
        'liked': liked
    })


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Postagem, id_postagem=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.postagem = post
            comment.user = request.user
            comment.save()

            # Converte o horário UTC para o fuso horário local definido em settings.py
            local_created_at = timezone.localtime(comment.created_at)

            return JsonResponse({
                'success': True,
                'comment': {
                    'content': comment.content,
                    'user': comment.user.username,
                    'created_at': local_created_at.strftime('%d/%m/%Y %H:%M')
                },
                'comments_count': post.comments.count()
            })
    return JsonResponse({'success': False, 'errors': form.errors if 'form' in locals() else 'Invalid request'})


@login_required
def delete_comment(request, comment_id):
    """
    View para excluir um comentário.
    Permite que o autor do comentário ou um superusuário o exclua.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.postagem.id_postagem
    
    # Verifica se o usuário é o autor do comentário ou um superusuário
    if comment.user != request.user and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Permissão negada'}, status=403)
    
    # Exclui o comentário
    comment.delete()
    
    # Atualiza a contagem de comentários
    post = get_object_or_404(Postagem, id_postagem=post_id)
    
    return JsonResponse({
        'success': True,
        'comments_count': post.comments.count()
    })