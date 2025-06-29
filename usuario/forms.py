from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from socialapp.models import Perfil

class UsuarioForm(UserCreationForm):
    FIRST_NAME_CHOICES = [
        ('Docente', 'Docente'),
        ('Discente', 'Discente')
    ]
    
    foto_perfil = forms.ImageField(
        label='Foto de Perfil',
        required=False,
        help_text='Faça upload de uma foto para o seu perfil (opcional)'
    )
    
    # Adicionando campo de data de nascimento
    data_nascimento = forms.DateField(
        label='Data de Nascimento',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        help_text='Selecione sua data de nascimento'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'last_name', 'first_name', 'data_nascimento', 'foto_perfil']
        
    username = forms.CharField(label='Matrícula:')
    email = forms.EmailField(label='E-mail:')
    last_name = forms.CharField(label='Nome Completo:')
    first_name = forms.ChoiceField(
        label='Status:',
        choices=FIRST_NAME_CHOICES,
        widget=forms.Select(attrs={'class': 'custom-select'}),
        initial='Discente'
    )
    
    def save(self, commit=True):
        # Primeiro, salva o usuário
        user = super().save(commit=False)
        if commit:
            user.save()
        
        # Obtém os dados do formulário
        data_nascimento = self.cleaned_data.get('data_nascimento')
        foto_perfil = self.cleaned_data.get('foto_perfil')
        
        # Garante que a data de nascimento não seja nula
        if not data_nascimento:
            data_nascimento = timezone.now().date()
        
        # Cria ou atualiza o perfil do usuário
        try:
            perfil = Perfil.objects.get(matricula_perfil=user.username)
            perfil.nome_perfil = user.last_name or user.username
            perfil.data_nascimento = data_nascimento
            if foto_perfil:  # Sobrepor a foto apenas se uma nova foi fornecida
                perfil.foto_perfil = foto_perfil
            perfil.save()
        except Perfil.DoesNotExist:
            Perfil.objects.create(
                matricula_perfil=user.username,
                nome_perfil=user.last_name or user.username,
                data_nascimento=data_nascimento,
                foto_perfil=foto_perfil
            )
        
        return user

