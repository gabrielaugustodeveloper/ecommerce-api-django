# Usar uma imagem base oficial do Python estável e leve
FROM python:3.11-slim

# Configurar variáveis de ambiente vitais para o comportamento do Python no Docker:
# 1. Impede que o Python escreva ficheiros .pyc no disco
# 2. Garante que o output do terminal seja exibido em tempo real (sem buffering)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Definir o diretório de trabalho interno do contentor
WORKDIR /app

# Instalar ferramentas de compilação essenciais do sistema operacional
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar o ficheiro de requisitos primeiro para otimizar o mecanismo de cache do Docker
COPY requirements.txt /app/

# Instalar as dependências da API isoladamente
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante código-fonte do projeto para o contentor
COPY . /app/

# Expor a porta padrão utilizada pelo servidor de desenvolvimento do Django
EXPOSE 8000

# Executar de forma sequencial as migrações da base de dados e iniciar o servidor
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]