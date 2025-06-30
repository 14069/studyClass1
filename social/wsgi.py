"""
WSGI config for social project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Configura as variáveis de ambiente antes de importar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social.settings')

# Importa e configura o Cloudinary
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Inicializa a aplicação WSGI
application = get_wsgi_application()

# Aplica o middleware do WhiteNoise para servir arquivos estáticos
from whitenoise import WhiteNoise
from pathlib import Path

# Obtém o diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configura o WhiteNoise para servir arquivos estáticos
application = WhiteNoise(
    application,
    root=os.path.join(BASE_DIR, 'staticfiles'),
    prefix='static/',
)

# Adiciona diretórios adicionais para o WhiteNoise, se necessário
application.add_files(os.path.join(BASE_DIR, 'static'), prefix='static/')
