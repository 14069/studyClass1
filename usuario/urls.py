from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import new_usuario, perfil_usuario, editar_perfil

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuario/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='social/home.html'), name='logout'),
    path('new_usuario/', new_usuario, name='new_usuario'),
    # URL para o próprio perfil
    path('perfil_usuario/', login_required(perfil_usuario), name='perfil_usuario'),
    # URL para editar o perfil
    path('editar_perfil/', login_required(editar_perfil), name='editar_perfil'),
]