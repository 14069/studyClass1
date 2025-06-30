# Estágio de construção (build)
FROM python:3.10-slim as builder

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instala as dependências do Python
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Estágio final
FROM python:3.10-slim

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/user/.local/bin:$PATH"

# Cria um usuário não-root
RUN useradd -m user && \
    mkdir -p /app/static && \
    chown -R user:user /app

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copia as wheels do estágio de construção
COPY --from=builder /app/wheels /wheels

# Instala as dependências do Python
RUN pip install --no-cache /wheels/*

# Copia o projeto
COPY . .

# Variáveis de ambiente
ENV SECRET_KEY=django-insecure-ry_-s8mnz=b3a*ykg3ebic3mv_l&0a3o_0el2h2zr13ze)@4)2f8$u$jnwud
ENV DEBUG=False
ENV ALLOWED_HOSTS=.railway.app,studyclass.up.railway.app
ENV CSRF_TRUSTED_ORIGINS=https://studyclass.up.railway.app
ENV DATABASE_URL=postgres://postgres:qkdRSNeYDAnTglsLAYBxRfqlnZoYSxPF@postgres.railway.internal:5432/railway

# Cria diretório para arquivos estáticos
RUN mkdir -p /app/staticfiles
RUN chown -R user:user /app/staticfiles


# Coleta arquivos estáticos
RUN python manage.py collectstatic --noinput

# Muda para o usuário não-root
USER user

# Comando para executar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "social.wsgi:application"]
