from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from socialapp.forms import AvaliaForms, PostagemForms, PerfilForms, TelefoneForms, PerfilPostForms, CommentForm
from socialapp.models import Avalia, Postagem, Perfil, Telefone, Perfil_post, Like, Comment
from django.http import JsonResponse, Http404, HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Avg, Count
import json

# Create your views here.
@login_required
def index(request):
    # Mostra todas as postagens para todos os usuários
    posts = Postagem.objects.all().order_by('-data_postagem')
    
    # Obtém os IDs dos posts curtidos pelo usuário
    liked_post_ids = Like.objects.filter(user=request.user).values_list('postagem_id', flat=True)
    comment_form = CommentForm()
    
    # Obtém todos os perfis para exibir as fotos de perfil
    perfis = Perfil.objects.select_related('user').all()
    
    # Obtém as avaliações do usuário para os posts
    user_ratings = {}
    if request.user.is_authenticated:
        ratings = Avalia.objects.filter(user=request.user, postagem__in=posts)
        user_ratings = {rating.postagem_id: rating.valor_avalia for rating in ratings}
    
    # Calcula a média de avaliações para cada post
    from django.db.models import Avg, Count
    posts_with_ratings = posts.annotate(
        avg_rating=Avg('avaliacoes__valor_avalia'),
        rating_count=Count('avaliacoes')
    )

    return render(request, 'social/index.html', {
        'posts': posts_with_ratings,
        'liked_post_ids': list(liked_post_ids),
        'comment_form': comment_form,
        'is_superuser': request.user.is_superuser,
        'current_user': request.user.username,
        'perfis': perfis,
        'user_ratings': user_ratings
    })

@login_required
def my_posts(request):
    # Mostra apenas as postagens do usuário logado
    posts = Postagem.objects.filter(autor_postagem=request.user.username).order_by('-data_postagem')
    
    # Obtém os IDs dos posts curtidos pelo usuário
    liked_post_ids = Like.objects.filter(user=request.user).values_list('postagem_id', flat=True)
    comment_form = CommentForm()
    
    # Obtém todos os perfis para exibir as fotos de perfil
    perfis = Perfil.objects.select_related('user').all()
    
    # Obtém as avaliações do usuário para os posts
    user_ratings = {}
    if request.user.is_authenticated:
        ratings = Avalia.objects.filter(user=request.user, postagem__in=posts)
        user_ratings = {rating.postagem_id: rating.valor_avalia for rating in ratings}
    
    # Calcula a média de avaliações para cada post
    from django.db.models import Avg
    posts_with_ratings = posts.annotate(
        avg_rating=Avg('avaliacoes__valor_avalia'),
        rating_count=Count('avaliacoes')
    )

    return render(request, 'social/my_posts.html', {
        'posts': posts_with_ratings,
        'liked_post_ids': list(liked_post_ids),
        'comment_form': comment_form,
        'is_superuser': request.user.is_superuser,
        'current_user': request.user.username,
        'perfis': perfis,
        'user_ratings': user_ratings
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

def home(request):
    postagens = Postagem.objects.all().order_by('-data_postagem')[:5]
    return render(request, 'social/home.html', {'postagens': postagens})

def contato(request):
    return render(request, 'social/contact.html')

def sobre(request):
    return render(request, 'social/about.html')

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
            try:
                # Cria a postagem sem salvar no banco ainda
                postagem = form.save(commit=False)
                # Define o autor como o nome de usuário
                postagem.autor_postagem = request.user.username
                # Define a data atual
                postagem.data_postagem = timezone.now()
                # Salva a postagem (isso também processa a imagem)
                postagem.save()
                
                messages.success(request, 'Postagem criada com sucesso!')
                return redirect('my_posts')
            except Exception as e:
                messages.error(request, f'Erro ao criar postagem: {str(e)}')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        # Inicializa o formulário com valores padrão
        form = PostagemForms(initial={
            'autor_postagem': request.user.username,
            'data_postagem': timezone.now()
        })
    
    # Mostra apenas as postagens do usuário atual
    posts = Postagem.objects.filter(autor_postagem=request.user.username).order_by('-data_postagem')
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
        messages.error(request, 'Você não tem permissão para editar esta postagem.')
        return redirect('index')
        
    # Mostra apenas as postagens do usuário atual
    posts = Postagem.objects.filter(autor_postagem=request.user.username).order_by('-data_postagem')

    if request.method == "POST":
        form = PostagemForms(request.POST, request.FILES, instance=post)
        if form.is_valid():
            try:
                # Verifica se o usuário marcou para remover a imagem
                if 'remove_imagem' in request.POST and request.POST['remove_imagem'] == 'on':
                    # Remove o arquivo de imagem do sistema de arquivos
                    if post.imagem_postagem:
                        post.imagem_postagem.delete(save=False)
                    # Remove a referência da imagem no banco de dados
                    post.imagem_postagem = None
                
                # Verifica se foi enviada uma nova imagem
                if 'imagem_postagem' in request.FILES:
                    # Remove a imagem antiga se existir
                    if post.imagem_postagem:
                        post.imagem_postagem.delete(save=False)
                
                # Salva as alterações
                post.save()
                
                messages.success(request, 'Postagem atualizada com sucesso!')
                return redirect('my_posts')
                
            except Exception as e:
                messages.error(request, f'Erro ao atualizar a postagem: {str(e)}')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = PostagemForms(instance=post)
    
    return render(request, 'social/editar_post.html', {
        'form': form, 
        'post': post,
        'posts': posts
    })



import logging
from django.db import transaction, connection
logger = logging.getLogger(__name__)

@login_required
def deleta_post(request, id):
    try:
        with transaction.atomic():
            # Primeiro, obtemos a postagem
            post = get_object_or_404(Postagem, pk=id)
            
            # Verifica se o usuário é o autor OU um superusuário
            is_author = str(post.autor_postagem) == str(request.user.username)
            is_superuser = request.user.is_superuser
            
            if not (is_author or is_superuser):
                messages.error(request, "Você não tem permissão para excluir esta postagem.")
                return redirect('index')

            if request.method == "POST":
                logger.info(f"Iniciando exclusão da postagem {post.id_postagem}")
                
                # 1. Primeiro, obtemos o ID da postagem
                post_id = post.id_postagem
                
                # 2. Excluir todos os relacionamentos conhecidos
                # Excluir comentários
                Comment.objects.filter(postagem=post).delete()
                
                # Excluir likes
                Like.objects.filter(postagem=post).delete()
                
                # Excluir ratings
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM socialapp_rating WHERE postagem_id = %s", [post_id])
                
                # Excluir perfis de post
                Perfil_post.objects.filter(id_postagem=post).delete()
                
                # 3. Forçar a limpeza do cache de relacionamentos
                post = Postagem.objects.get(pk=post_id)
                
                # 4. Remover a imagem associada à postagem, se existir
                if post.imagem_postagem:
                    try:
                        # Remove o arquivo de imagem do sistema de arquivos
                        post.imagem_postagem.delete(save=False)
                        logger.info(f"Imagem da postagem {post_id} removida com sucesso.")
                    except Exception as e:
                        logger.error(f"Erro ao remover a imagem da postagem {post_id}: {str(e)}", exc_info=True)
                
                # 5. Excluir a postagem
                logger.info("Excluindo a postagem...")
                post.delete()
                
                messages.success(request, "Postagem excluída com sucesso!")
                
                # Redireciona para a página correta com base no parâmetro 'next' ou para a página inicial
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
            
            return redirect('index')
            
    except Exception as e:
        logger.error(f"Erro ao excluir postagem: {str(e)}", exc_info=True)
        messages.error(request, f"Ocorreu um erro ao excluir a postagem: {str(e)}")
        return redirect('index')


@login_required
def like_post(request, post_id):
    print(f"[DEBUG] like_post chamado para post_id: {post_id}")
    try:
        post = get_object_or_404(Postagem, id_postagem=post_id)
        print(f"[DEBUG] Post encontrado: {post.titulo_postagem}")
        
        like, created = Like.objects.get_or_create(user=request.user, postagem=post)
        print(f"[DEBUG] Like criado: {created}")

        if not created:
            # Se o like já existia, o usuário está descurtindo.
            like.delete()
            liked = False
            print("[DEBUG] Like removido")
        else:
            # Se o like foi criado agora, o usuário está curtindo.
            liked = True
            print("[DEBUG] Like adicionado")

        likes_count = post.likes.count()
        print(f"[DEBUG] Total de likes: {likes_count}")

        # Retorna a nova contagem de likes e o status atual do like do usuário
        response_data = {
            'success': True,
            'likes_count': likes_count,
            'liked': liked
        }
        print(f"[DEBUG] Retornando resposta: {response_data}")
        return JsonResponse(response_data)
        
    except Exception as e:
        print(f"[ERROR] Erro em like_post: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


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
                    'id': comment.id,
                    'content': comment.content,
                    'user': comment.user.username,
                    'created_at': local_created_at.strftime('%d/%m/%Y %H:%M'),
                    'is_owner': comment.user == request.user
                },
                'comments_count': post.comments.count()
            })
    return JsonResponse({'success': False, 'errors': form.errors if 'form' in locals() else 'Invalid request'})


@login_required
def load_more_comments(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Postagem, id_postagem=post_id)
        page = int(request.GET.get('page', 1))
        comments_per_page = 5
        
        # Calcula o offset baseado na página
        offset = (page - 1) * comments_per_page
        
        # Pega os comentários com limite e offset
        comments = post.comments.all().order_by('created_at')[offset:offset + comments_per_page]
        
        # Prepara a lista de comentários para o JSON
        comments_data = [{
            'id': comment.id,
            'content': comment.content,
            'user': comment.user.username,
            'created_at': timezone.localtime(comment.created_at).strftime('%d/%m/%Y %H:%M'),
            'is_owner': comment.user == request.user
        } for comment in comments]
        
        # Verifica se há mais comentários para carregar
        has_more = post.comments.count() > (offset + comments_per_page)
        
        return JsonResponse({
            'success': True,
            'comments': comments_data,
            'has_more': has_more,
            'next_page': page + 1 if has_more else None
        })
    return JsonResponse({'success': False, 'errors': 'Invalid request'})


@login_required
def delete_comment(request, comment_id):
    """
    View para excluir um comentário.
    Permite que o autor do comentário ou um superusuário o exclua.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.postagem.id
    
    # Verifica se o usuário tem permissão para excluir o comentário
    if request.user != comment.user and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Você não tem permissão para excluir este comentário.'}, status=403)
    
    comment.delete()
    
    # Atualiza a contagem de comentários
    comment_count = Comment.objects.filter(postagem_id=post_id).count()
    
    return JsonResponse({
        'success': True,
        'comment_count': comment_count
    })


@require_POST
@login_required
def rate_post(request, post_id):
    """
    View para avaliar um post com estrelas.
    """
    try:
        data = json.loads(request.body)
        rating = int(data.get('rating'))
        
        # Valida a avaliação (deve estar entre 1 e 5)
        if rating not in [1, 2, 3, 4, 5]:
            return JsonResponse({'success': False, 'error': 'Avaliação inválida'}, status=400)
        
        # Obtém o post
        post = get_object_or_404(Postagem, id_postagem=post_id)
        
        # Verifica se o usuário já avaliou este post
        rating_obj, created = Avalia.objects.get_or_create(
            user=request.user,
            postagem=post,
            defaults={'valor_avalia': rating}
        )
        
        # Se não for uma nova avaliação, atualiza a existente
        if not created:
            rating_obj.valor_avalia = rating
            rating_obj.save()
        
        # Recalcula a média de avaliações
        ratings = Avalia.objects.filter(postagem=post)
        avg_rating = ratings.aggregate(Avg('valor_avalia'))['valor_avalia__avg']
        rating_count = ratings.count()
        
        return JsonResponse({
            'success': True,
            'avg_rating': round(avg_rating, 1) if avg_rating else 0,
            'rating_count': rating_count,
            'user_rating': rating
        })
        
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'success': False, 'error': 'Dados inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def get_post_ratings(request, post_id):
    """
    Retorna as estatísticas de avaliação de um post.
    """
    try:
        post = get_object_or_404(Postagem, id_postagem=post_id)
        
        # Calcula a média e contagem de avaliações
        ratings = Avalia.objects.filter(postagem=post)
        avg_rating = ratings.aggregate(Avg('valor_avalia'))['valor_avalia__avg']
        rating_count = ratings.count()
        
        # Verifica se o usuário atual já avaliou o post
        user_rating = None
        if request.user.is_authenticated:
            try:
                user_rating = Avalia.objects.get(user=request.user, postagem=post).valor_avalia
            except Avalia.DoesNotExist:
                pass
        
        return JsonResponse({
            'success': True,
            'avg_rating': round(avg_rating, 1) if avg_rating else 0,
            'rating_count': rating_count,
            'user_rating': user_rating
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)