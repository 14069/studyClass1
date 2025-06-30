from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Avaliação das postagens
class Avalia(models.Model):
    id_avalia = models.AutoField(primary_key=True)
    valor_avalia = models.IntegerField(
        choices=[(1, '1 Estrela'), (2, '2 Estrelas'), (3, '3 Estrelas'), (4, '4 Estrelas'), (5, '5 Estrelas')]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postagem = models.ForeignKey('Postagem', on_delete=models.CASCADE, related_name='avaliacoes')
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'postagem')
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'

    def __str__(self):
        return f"{self.user.username} - {self.get_valor_avalia_display()}"


# Postagens
class Postagem(models.Model):
    id_postagem = models.AutoField(primary_key=True)
    autor_postagem = models.CharField(max_length=255)
    data_postagem = models.DateTimeField(auto_now_add=True)
    titulo_postagem = models.CharField(max_length=200)
    conteudo_postagem = models.TextField()


    def __str__(self):
        return self.titulo_postagem


# Perfil do usuário
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil', null=True, blank=True)
    id_perfil = models.AutoField(primary_key=True)
    nome_perfil = models.CharField(max_length=255, default='Usuário')
    data_nascimento = models.DateField(null=True, blank=True, default=timezone.now)
    matricula_perfil = models.CharField(max_length=255, unique=True, null=True, blank=True)
    numero_telefone = models.CharField('Telefone', max_length=20, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['-data_criacao']

    def __str__(self):
        return self.nome_perfil



# Telefone vinculado ao perfil
class Telefone(models.Model):
    id_telefone = models.AutoField(primary_key=True)
    numero_telefone = models.CharField(max_length=255)
    id_perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='id_perfil')

    def __str__(self):
        return self.numero_telefone


# Relacionamento entre perfil e postagem
class Perfil_post(models.Model):
    id_perfil_post = models.AutoField(primary_key=True)
    id_perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='id_perfil')
    id_postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE, db_column='id_postagem')

    def __str__(self):
        return str(self.id_perfil)


# Curtidas
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'postagem')

    def __str__(self):
        return f'{self.user.username} curtiu "{self.postagem.titulo_postagem}"'


# Comentários
class Comment(models.Model):
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comentário de {self.user.username} em "{self.postagem}"'
