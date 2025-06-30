from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from socialapp.views import (
    index, sobre, home, contato,
    new_avalia, editar_avalia, deleta_avalia, rate_post, get_post_ratings,
    new_post, deleta_post, editar_post, like_post, add_comment, delete_comment,
    load_more_comments, my_posts, perfil_usuario
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url='/static/assets/favicon.ico')),

    # Rotas principais
    path('', home, name='home'),
    path('index/', index, name='index'),
    path('home/', home, name='home'),
    path('sobre/', sobre, name='sobre'),
    path('contato/', contato, name='contato'),

    # Avaliações
    path('new_avalia/', new_avalia, name='new_avalia'),
    path('editar_avalia/<str:id>/', editar_avalia, name='editar_avalia'),
    path('deleta_avalia/<int:id>/', deleta_avalia, name='deleta_avalia'),

    # Postagens
    path('new_post/', new_post, name='new_post'),
    path('editar_post/<str:id>/', editar_post, name='editar_post'),
    path('deleta_post/<int:id>/', deleta_post, name='deleta_post'),

    # Interações com postagens
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('post/<int:post_id>/load-more-comments/', load_more_comments, name='load_more_comments'),
    path('post/<int:post_id>/rate/', rate_post, name='rate_post'),
    path('post/<int:post_id>/ratings/', get_post_ratings, name='get_post_ratings'),

    # Perfil e postagens do usuário
    path('minhas-postagens/', my_posts, name='my_posts'),
    path('perfil/', perfil_usuario, name='perfil_usuario'),
    path('perfil/<str:username>/', perfil_usuario, name='view_profile'),

    # Autenticação
    path('', include('usuario.urls')),
]

# Servir arquivos estáticos e mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
