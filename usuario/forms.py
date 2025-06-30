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
    

    # Adicionando campo de data de nascimento
    data_nascimento = forms.DateField(
        label='Data de Nascimento',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        help_text='Selecione sua data de nascimento'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'last_name', 'first_name', 'data_nascimento', 'numero_telefone']
        
    username = forms.CharField(label='Matrícula:')
    email = forms.EmailField(label='E-mail:')
    last_name = forms.CharField(label='Nome Completo:')
    first_name = forms.ChoiceField(
        label='Status:',
        choices=FIRST_NAME_CHOICES,
        widget=forms.Select(attrs={'class': 'custom-select'}),
        initial='Discente'
    )
    numero_telefone = forms.CharField(
        label='Telefone:',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
        help_text='Número de telefone com DDD (opcional)'
    )
    
    def save(self, commit=True):
        # Primeiro, salva o usuário
        user = super().save(commit=False)
        if commit:
            user.save()
        
        # Obtém os dados do formulário
        data_nascimento = self.cleaned_data.get('data_nascimento')
        numero_telefone = self.cleaned_data.get('numero_telefone')
        
        # Garante que a data de nascimento não seja nula
        if not data_nascimento:
            data_nascimento = timezone.now().date()
        
        # Cria ou atualiza o perfil do usuário
        try:
            perfil = Perfil.objects.get(matricula_perfil=user.username)
            perfil.nome_perfil = user.last_name or user.username
            perfil.data_nascimento = data_nascimento
            perfil.save()
        except Perfil.DoesNotExist:
            perfil = Perfil.objects.create(
                matricula_perfil=user.username,
                nome_perfil=user.last_name or user.username,
                data_nascimento=data_nascimento,
                numero_telefone=numero_telefone
            )
        
        return user


class EditarPerfilForm(forms.ModelForm):
    """
    Formulário para edição do perfil do usuário.
    Inclui campos para atualizar informações básicas e senha.
    """
    # Campo para telefone
    numero_telefone = forms.CharField(
        label='Telefone',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
        help_text='Número de telefone com DDD (opcional)'
    )
    
    data_nascimento = forms.DateField(
        label='Data de Nascimento',
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Selecione sua data de nascimento'
    )
    
    # Campos para alteração de senha
    current_password = forms.CharField(
        label='Senha Atual',
        widget=forms.PasswordInput,
        required=False,
        help_text='Digite sua senha atual para confirmar as alterações (obrigatório para alterar senha)'
    )
    
    nova_senha1 = forms.CharField(
        label='Nova Senha',
        widget=forms.PasswordInput,
        required=False,
        help_text='Deixe em branco para manter a senha atual'
    )
    
    nova_senha2 = forms.CharField(
        label='Confirmação da Nova Senha',
        widget=forms.PasswordInput,
        required=False,
        help_text='Repita a nova senha'
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'numero_telefone', 'data_nascimento']
        labels = {
            'first_name': 'Status',
            'last_name': 'Nome Completo',
            'email': 'E-mail',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define as classes CSS para os campos
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Adiciona placeholder específico para o campo de email
        self.fields['email'].widget.attrs['placeholder'] = 'seu@email.com'
        
        # Define as opções para o campo first_name (status)
        self.fields['first_name'].widget = forms.Select(
            choices=[
                ('Docente', 'Docente'),
                ('Discente', 'Discente')
            ],
            attrs={'class': 'form-select'}
        )
    
    def clean(self):
        cleaned_data = super().clean()
        nova_senha1 = cleaned_data.get('nova_senha1')
        nova_senha2 = cleaned_data.get('nova_senha2')
        current_password = cleaned_data.get('current_password')
        
        # Validação da mudança de senha
        if nova_senha1 or nova_senha2:
            if not current_password:
                self.add_error('current_password', 'Você deve informar sua senha atual para alterar a senha.')
            
            if nova_senha1 != nova_senha2:
                self.add_error('nova_senha2', 'As senhas não conferem.')
            
            if current_password and not self.instance.check_password(current_password):
                self.add_error('current_password', 'Senha atual incorreta.')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Se uma nova senha foi fornecida, atualiza a senha
        nova_senha = self.cleaned_data.get('nova_senha1')
        if nova_senha:
            user.set_password(nova_senha)
        
        if commit:
            user.save()
        
        return user
