# Etapa 1: Imagem base do Python
FROM python:3.9-slim

# Etapa 2: Configurar variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0

# Etapa 3: Criar e definir o diretório de trabalho
WORKDIR /app

# Etapa 4: Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Etapa 5: Copiar os arquivos necessários para o contêiner
COPY requirements.txt /app/

# Etapa 6: Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 7: Copiar o restante do código da aplicação
COPY . /app

# Etapa 8: Expor a porta 8080
EXPOSE 8080

# Etapa 9: Comando de inicialização
["python", "app.py"]
