from django.db import migrations, models
from django.conf import settings
import django.utils.timezone

def popular_avaliacoes(apps, schema_editor):
    # Esta função será usada para popular os dados iniciais
    Avalia = apps.get_model('socialapp', 'Avalia')
    User = apps.get_model(settings.AUTH_USER_MODEL)
    Postagem = apps.get_model('socialapp', 'Postagem')
    
    # Se houver avaliações sem usuário ou postagem, podemos atribuir valores padrão
    # Neste exemplo, estamos atribuindo o primeiro usuário e a primeira postagem disponíveis
    # Você pode personalizar esta lógica conforme necessário
    try:
        default_user = User.objects.first()
        default_post = Postagem.objects.first()
        
        if default_user and default_post:
            # Atualiza todas as avaliações existentes com valores padrão
            Avalia.objects.filter(user__isnull=True).update(user=default_user)
            Avalia.objects.filter(postagem__isnull=True).update(postagem=default_post)
    except Exception as e:
        print(f"Erro ao popular avaliações: {e}")

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialapp', '0006_perfil_user_alter_perfil_matricula_perfil'),
    ]

    operations = [
        migrations.AddField(
            model_name='avalia',
            name='data_avaliacao',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='avalia',
            name='postagem',
            field=models.ForeignKey(
                'socialapp.Postagem',
                on_delete=models.CASCADE,
                related_name='avaliacoes',
                null=True,  # Permite nulo temporariamente
            ),
        ),
        migrations.AddField(
            model_name='avalia',
            name='user',
            field=models.ForeignKey(
                settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                null=True,  # Permite nulo temporariamente
            ),
        ),
        migrations.RunPython(popular_avaliacoes),
        # Torna os campos obrigatórios após a migração dos dados
        migrations.AlterField(
            model_name='avalia',
            name='postagem',
            field=models.ForeignKey(
                'socialapp.Postagem',
                on_delete=models.CASCADE,
                related_name='avaliacoes',
            ),
        ),
        migrations.AlterField(
            model_name='avalia',
            name='user',
            field=models.ForeignKey(
                settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
            ),
        ),
        # Adiciona a restrição de unicidade
        migrations.AlterUniqueTogether(
            name='avalia',
            unique_together={('user', 'postagem')},
        ),
    ]