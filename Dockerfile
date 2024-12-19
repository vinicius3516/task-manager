# Usa uma imagem oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos do projeto para o contêiner
COPY . /app

# Instala as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 8080 (Cloud Run requer essa porta)
EXPOSE 8080

# Define o comando para rodar sua aplicação
CMD ["python", "app.py"]
