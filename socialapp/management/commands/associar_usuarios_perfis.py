from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from socialapp.models import Perfil

User = get_user_model()

class Command(BaseCommand):
    help = 'Associa usuários existentes aos seus perfis com base no nome de usuário'

    def handle(self, *args, **options):
        # Obtém todos os usuários
        usuarios = User.objects.all()
        
        for usuario in usuarios:
            # Tenta encontrar um perfil com o nome de usuário correspondente
            try:
                perfil = Perfil.objects.get(nome_perfil=usuario.username)
                if not perfil.user:  # Só associa se o perfil não tiver um usuário associado
                    perfil.user = usuario
                    perfil.save()
                    self.stdout.write(self.style.SUCCESS(f'Associado usuário {usuario.username} ao perfil {perfil.nome_perfil}'))
            except Perfil.DoesNotExist:
                # Se não existir um perfil, cria um novo
                perfil = Perfil.objects.create(
                    user=usuario,
                    nome_perfil=usuario.username,
                    matricula_perfil=f'mat_{usuario.id}'  # Você pode ajustar isso conforme necessário
                )
                self.stdout.write(self.style.SUCCESS(f'Criado novo perfil para o usuário {usuario.username}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro ao processar usuário {usuario.username}: {str(e)}'))
