# Generated by Django 5.1.7 on 2025-06-30 06:49

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Postagem',
            fields=[
                ('id_postagem', models.AutoField(primary_key=True, serialize=False)),
                ('autor_postagem', models.CharField(max_length=255)),
                ('data_postagem', models.DateTimeField(auto_now_add=True)),
                ('titulo_postagem', models.CharField(max_length=200)),
                ('conteudo_postagem', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id_perfil', models.AutoField(primary_key=True, serialize=False)),
                ('nome_perfil', models.CharField(default='Usuário', max_length=255)),
                ('data_nascimento', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('matricula_perfil', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('numero_telefone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfis',
                'ordering': ['-data_criacao'],
            },
        ),
        migrations.CreateModel(
            name='Perfil_post',
            fields=[
                ('id_perfil_post', models.AutoField(primary_key=True, serialize=False)),
                ('id_perfil', models.ForeignKey(db_column='id_perfil', on_delete=django.db.models.deletion.DO_NOTHING, to='socialapp.perfil')),
                ('id_postagem', models.ForeignKey(db_column='id_postagem', on_delete=django.db.models.deletion.CASCADE, to='socialapp.postagem')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('postagem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='socialapp.postagem')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Telefone',
            fields=[
                ('id_telefone', models.AutoField(primary_key=True, serialize=False)),
                ('numero_telefone', models.CharField(max_length=255)),
                ('id_perfil', models.ForeignKey(db_column='id_perfil', on_delete=django.db.models.deletion.DO_NOTHING, to='socialapp.perfil')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('postagem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='socialapp.postagem')),
            ],
            options={
                'unique_together': {('user', 'postagem')},
            },
        ),
        migrations.CreateModel(
            name='Avalia',
            fields=[
                ('id_avalia', models.AutoField(primary_key=True, serialize=False)),
                ('valor_avalia', models.IntegerField(choices=[(1, '1 Estrela'), (2, '2 Estrelas'), (3, '3 Estrelas'), (4, '4 Estrelas'), (5, '5 Estrelas')])),
                ('data_avaliacao', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('postagem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avaliacoes', to='socialapp.postagem')),
            ],
            options={
                'verbose_name': 'Avaliação',
                'verbose_name_plural': 'Avaliações',
                'unique_together': {('user', 'postagem')},
            },
        ),
    ]
