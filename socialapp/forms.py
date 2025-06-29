from django import forms
from socialapp.models import Avalia, Postagem, Perfil, Telefone, Perfil_post, Comment

class AvaliaForms(forms.ModelForm):
    class Meta:
        model = Avalia
        fields ="__all__"


class PostagemForms(forms.ModelForm):
    class Meta:
        model = Postagem
        fields = ['titulo_postagem', 'conteudo_postagem', 'imagem_postagem']
        widgets = {
            'titulo_postagem': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Título da postagem',
                'required': True
            }),
            'conteudo_postagem': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'rows': 4,
                'placeholder': 'O que você está pensando?',
                'required': True
            }),
            'imagem_postagem': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'imagem-postagem',
                'onchange': 'previewImage(this)'
            })
        }
        labels = {
            'titulo_postagem': 'Título',
            'conteudo_postagem': 'Conteúdo',
            'imagem_postagem': 'Imagem (opcional)'
        }
        help_texts = {
            'imagem_postagem': 'Formatos suportados: JPG, JPEG, PNG. Tamanho máximo: 5MB.'
        }


class PerfilForms(forms.ModelForm):
    class Meta:
        model = Perfil
        fields ="__all__"


class TelefoneForms(forms.ModelForm):
    class Meta:
        model = Telefone
        fields ="__all__"
        widgets = {
            'numero_telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PerfilPostForms(forms.ModelForm):
    class Meta:
        model = Perfil_post
        fields ="__all__"
        widgets = {
            'id_perfil': forms.Select(attrs={'class': 'form-control'}),
            'id_postagem': forms.Select(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm rounded-pill',
                    'placeholder': 'Adicione um comentário...',
                    'aria-label': 'Adicionar comentário'
                }
            )
        }

