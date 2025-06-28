

from django.shortcuts import render, redirect, get_object_or_404
from socialapp.forms import AvaliaForms,PostagemForms,PerfilForms, TelefoneForms, PerfilPostForms
from socialapp.models import Avalia, Postagem, Perfil, Telefone, Perfil_post, Like, Comment
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def index(request):
    posts = Postagem.objects.all().order_by('-data_postagem')
    liked_post_ids = Like.objects.filter(user=request.user).values_list('postagem_id', flat=True)

    return render(request, 'social/index.html', {
        'posts': posts,
        'liked_post_ids': liked_post_ids
    })

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
            return redirect('index')
    else:
        form = PostagemForms()
    
    posts = Postagem.objects.all().order_by('-data_postagem')
    return render(request, 'social/new_post.html', {'form': form, 'posts': posts})


def editar_post(request, id):
    post =get_object_or_404(Postagem, pk=id)
    form =PostagemForms(instance=post)
    posts =Postagem.objects.all()

    if(request.method =="POST"):
        form = PostagemForms(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('new_post')
        return render(request, 'social/editar_post.html', {'form': form, 'posts': posts, 'post':post})
    else:
        return render(request, 'social/editar_post.html', {'form': form, 'posts': posts, 'post':post})



def deleta_post(request,id):
    post = get_object_or_404(Postagem, pk=id)


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
    form = PostagemForms(instance=post)
    posts = Postagem.objects.all()
    if request.method == "POST":
        post.delete()
        return redirect('new_post')
    return render(request,'social/deleta_post.html',{'post':post, 'form':form, 'posts':posts})