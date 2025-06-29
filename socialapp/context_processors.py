from .models import Perfil

def user_profile(request):
    """Adiciona o perfil do usuário ao contexto do template."""
    context = {}
    if hasattr(request, 'user') and request.user.is_authenticated:
        try:
            # Busca pelo matricula_perfil que é igual ao username do usuário
            context['user_profile'] = Perfil.objects.get(matricula_perfil=request.user.username)
        except Perfil.DoesNotExist:
            # Se não encontrar, tenta criar um perfil básico
            try:
                context['user_profile'] = Perfil.objects.create(
                    matricula_perfil=request.user.username,
                    nome_perfil=request.user.get_full_name() or request.user.username,
                )
            except Exception as e:
                print(f"Erro ao criar perfil: {e}")
                context['user_profile'] = None
    return context
