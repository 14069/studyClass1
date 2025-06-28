"""
URL configuration for social project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from socialapp.views import index, sobre, home, contato 
from socialapp.views import new_avalia, editar_avalia, deleta_avalia
from socialapp.views import new_post, deleta_post, editar_post, like_post, add_comment, delete_comment, my_posts, perfil_usuario, editar_perfil

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url='/static/assets/favicon.ico')),
    path('index/', index, name='index'),
    path('home/', home, name='home'),
    path('sobre/', sobre, name='sobre'),
    path('contato/', contato, name='contato'),
    path('new_avalia/', new_avalia, name='new_avalia'),
    path('editar_avalia/<str:id>', editar_avalia, name='editar_avalia'),
    path('deleta_avalia/<int:id>', deleta_avalia, name='deleta_avalia'),
    #post
    path('new_post/', new_post, name='new_post'),
    path('editar_post/<str:id>', editar_post, name='editar_post'),
    path('deleta_post/<int:id>', deleta_post, name='deleta_post'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('minhas-postagens/', my_posts, name='my_posts'),
    path('perfil/', perfil_usuario, name='perfil_usuario'),
    path('perfil/<str:username>/', perfil_usuario, name='view_profile'),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),

    path('', include('usuario.urls')),



]
