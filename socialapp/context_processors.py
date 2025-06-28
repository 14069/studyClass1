from .models import Perfil

def user_profile(request):
    """Adiciona o perfil do usuário ao contexto do template."""
    context = {}
    if hasattr(request, 'user') and request.user.is_authenticated:
        try:
            context['user_profile'] = Perfil.objects.get(nome_perfil=request.user.username)
        except Perfil.DoesNotExist:
            context['user_profile'] = None
    return context
