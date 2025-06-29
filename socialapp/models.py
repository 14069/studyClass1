

from django.db import models
from PIL import  Image
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Avalia(models.Model):
    id_avalia = models.AutoField(primary_key=True)
    valor_avalia = models.IntegerField(choices=[(1, '1 Estrela'), (2, '2 Estrelas'), (3, '3 Estrelas'), (4, '4 Estrelas'), (5, '5 Estrelas')])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postagem = models.ForeignKey('Postagem', on_delete=models.CASCADE, related_name='avaliacoes')
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'postagem')
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'

    def __str__(self):
        return f"{self.user.username} - {self.get_valor_avalia_display()}"

def post_image_path(instance, filename):
    # Upload para: posts/ano/mes/nome_do_arquivo
    import os
    from django.utils.timezone import now
    
    # Obtém a data atual para organizar em pastas
    date_path = now().strftime('posts/%Y/%m')
    # Gera um nome único para o arquivo
    filename_base, filename_ext = os.path.splitext(filename)
    unique_filename = f"{filename_base}_{now().strftime('%Y%m%d%H%M%S')}{filename_ext}"
    
    return os.path.join(date_path, unique_filename)

class Postagem(models.Model):
    id_postagem = models.AutoField(primary_key=True)
    autor_postagem = models.CharField(max_length=255)
    data_postagem = models.DateTimeField(auto_now_add=True)
    titulo_postagem = models.CharField(max_length=200)
    conteudo_postagem = models.TextField()
    imagem_postagem = models.ImageField(upload_to=post_image_path, blank=True, null=True, verbose_name='Imagem da Postagem')

    def __str__(self):
        return self.titulo_postagem
        
    def save(self, *args, **kwargs):
        # Primeiro, salva o modelo para obter o ID se for uma nova instância
        super().save(*args, **kwargs)
        
        # Se houver uma imagem, redimensiona
        if self.imagem_postagem:
            try:
                img = Image.open(self.imagem_postagem.path)
                
                # Define o tamanho máximo da imagem
                max_size = (1200, 1200)
                
                # Redimensiona mantendo a proporção
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Se a imagem for muito grande, corta o excesso
                if img.height > max_size[1] or img.width > max_size[0]:
                    # Calcula o ponto de corte centralizado
                    left = (img.width - max_size[0])/2 if img.width > max_size[0] else 0
                    top = (img.height - max_size[1])/2 if img.height > max_size[1] else 0
                    right = left + max_size[0] if left > 0 else img.width
                    bottom = top + max_size[1] if top > 0 else img.height
                    
                    img = img.crop((left, top, right, bottom))
                
                # Salva a imagem otimizada
                img.save(self.imagem_postagem.path, optimize=True, quality=85)
            except Exception as e:
                # Se ocorrer algum erro ao processar a imagem, apenas continue
                print(f"Erro ao processar imagem: {e}")

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil', null=True, blank=True)
    id_perfil = models.AutoField(primary_key=True)
    nome_perfil = models.CharField(max_length=255, default='Usuário')
    data_nascimento = models.DateField(null=True, blank=True, default=timezone.now)
    matricula_perfil = models.CharField(max_length=255, unique=True, null=True, blank=True)
    numero_telefone = models.CharField('Telefone', max_length=20, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfis/', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['-data_criacao']

    def __str__(self):
        return self.nome_perfil

    def save(self, *args, **kwargs):
        # Se for uma atualização, obtém a instância antiga para verificar se a foto mudou
        if self.pk:
            old_instance = Perfil.objects.get(pk=self.pk)
            if old_instance.foto_perfil and old_instance.foto_perfil != self.foto_perfil:
                # Remove o arquivo de imagem antigo
                old_instance.foto_perfil.delete(save=False)
        
        # Primeiro salva o modelo
        super().save(*args, **kwargs)
        
        # Se houver uma foto de perfil, redimensiona
        if self.foto_perfil:
            try:
                img = Image.open(self.foto_perfil.path)
                if img.height > 400 or img.width > 400:  # Redimensiona apenas se for maior que 400px
                    output_size = (400, 400)
                    img.thumbnail(output_size)
                    img.save(self.foto_perfil.path, quality=85)  # Salva com qualidade de 85% para reduzir o tamanho
            except Exception as e:
                # Se houver algum erro ao processar a imagem, apenas registre o erro
                print(f"Erro ao processar a imagem: {e}")

    def foto_url(self):
        if self.foto_perfil and hasattr(self.foto_perfil, 'url'):
            return self.foto_perfil.url
        else:
            return self.nome_perfil

class Telefone(models.Model):
    id_telefone = models.AutoField(primary_key=True)
    numero_telefone = models.CharField(max_length=255)
    id_perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='id_perfil')

    def __str__(self):
        return self.numero_telefone

class Perfil_post(models.Model):
    id_perfil_post = models.AutoField(primary_key=True)
    id_perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='id_perfil')
    id_postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE, db_column='id_postagem')

    def __str__(self):
        return str(self.id_perfil)

# Modelo para registrar as curtidas (likes)
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Garante que um usuário só pode curtir um post uma única vez
        unique_together = ('user', 'postagem')

    def __str__(self):
        return f'{self.user.username} curtiu "{self.postagem.titulo_postagem}"'

# Modelo para os comentários
class Comment(models.Model):
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at'] # Ordena os comentários do mais antigo para o mais novo

    def __str__(self):
        return f'Comentário de {self.user.username} em "{self.postagem}"'