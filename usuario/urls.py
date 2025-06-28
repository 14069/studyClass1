from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import new_usuario, perfil_usuario

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuario/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='social/home.html'), name='logout'),
    path('new_usuario/', new_usuario, name='new_usuario'),
    path('perfil_usuario/', login_required(perfil_usuario), name='perfil_usuario'),
]