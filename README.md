# Social Network App

Uma aplicação de rede social desenvolvida com Django.

## Recursos

- Autenticação de usuários
- Criação de postagens
- Comentários em postagens
- Sistema de avaliação por estrelas
- Upload de imagens
- Interface responsiva

## Pré-requisitos

- Python 3.10+
- pip (gerenciador de pacotes do Python)
- Git
- Conta no [Railway](https://railway.app/) para deploy

## Instalação Local

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/social-network.git
   cd social-network
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   # No Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # No Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```
   DEBUG=True
   SECRET_KEY=sua_chave_secreta_aqui
   DATABASE_URL=sqlite:///db.sqlite3
   ALLOWED_HOSTS=localhost,127.0.0.1
   CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
   ```

5. Execute as migrações:
   ```bash
   python manage.py migrate
   ```

6. Crie um superusuário:
   ```bash
   python manage.py createsuperuser
   ```

7. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

8. Acesse o site em: http://127.0.0.1:8000/

## Implantação no Railway

1. Faça login na sua conta do [Railway](https://railway.app/)
2. Crie um novo projeto
3. Adicione um novo serviço "Deploy from GitHub repo"
4. Selecione o repositório do projeto
5. Configure as variáveis de ambiente no painel do Railway:
   - `DEBUG`: `False`
   - `SECRET_KEY`: Uma chave secreta forte
   - `DATABASE_URL`: Será fornecida automaticamente quando você adicionar um banco de dados PostgreSQL
   - `ALLOWED_HOSTS`: `*` (ou seu domínio personalizado)
   - `CSRF_TRUSTED_ORIGINS`: `https://*.railway.app` (e seu domínio personalizado, se aplicável)
6. Ative o deploy automático

## Estrutura do Projeto

- `social/`: Configurações principais do projeto Django
- `socialapp/`: Aplicação principal
  - `migrations/`: Migrações do banco de dados
  - `static/`: Arquivos estáticos (CSS, JS, imagens)
  - `templates/`: Templates HTML
  - `models.py`: Modelos de dados
  - `views.py`: Lógica das visualizações
  - `urls.py`: Configuração de URLs
  - `forms.py`: Formulários
  - `admin.py`: Configuração do painel de administração
  - `context_processors.py`: Processadores de contexto
  - `templatetags/`: Tags de template personalizadas

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
