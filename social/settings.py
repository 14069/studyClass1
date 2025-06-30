from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env logo no início
load_dotenv()

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta (sempre tire do código no repo)
SECRET_KEY = os.getenv('SECRET_KEY', 'xx8xnfk0-7!40=^osbwtl9@bgb1d*ty7f(aq_*-3&zwgvys0)p')

# DEBUG (converte string para bool)
DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 'yes']

# Hosts permitidos (limpa espaços e entradas vazias)
ALLOWED_HOSTS = list(set([
    *[host.strip() for host in os.getenv('ALLOWED_HOSTS', '').split(',') if host.strip()],
    'studyclass.up.railway.app'
]))

# Origens confiáveis para CSRF
CSRF_TRUSTED_ORIGINS = list(set([
    *[origin.strip() for origin in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if origin.strip()],
    'https://studyclass.up.railway.app'
]))

# Diretório dos templates
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# Configuração do banco, usando DATABASE_URL do .env ou fallback SQLite local
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600,
        ssl_require=not DEBUG
    )
}

# Configurações estáticas
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'socialapp', 'static')]

# Demais configurações (INSTALLED_APPS, MIDDLEWARE, TEMPLATES, LOGGING etc) ...
# você pode deixar exatamente como já tem no seu arquivo

# Configurações de segurança para produção (só ativa quando DEBUG=False)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = 'DENY'

# Outros settings que você já tem (LOGIN_URL, LANGUAGE_CODE, TIME_ZONE, etc)



LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'home'
LOGOUT_REQUEST_METHOD = 'POST'

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
