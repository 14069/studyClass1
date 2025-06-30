"""
WSGI config for social project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from pathlib import Path

# Configura as variáveis de ambiente antes de importar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social.settings')

# Inicializa a aplicação WSGI
application = get_wsgi_application()

# Obtém o diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configura o WhiteNoise para servir arquivos estáticos
application = WhiteNoise(application)

# Adiciona o diretório de arquivos estáticos
application.add_files(os.path.join(BASE_DIR, 'staticfiles'), prefix='static/')

# Adiciona o diretório de mídia (apenas para desenvolvimento)
if os.getenv('ENVIRONMENT') == 'development':
    application.add_files(os.path.join(BASE_DIR, 'media'), prefix='media/')
