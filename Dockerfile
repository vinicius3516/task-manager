FROM python:3.12.3

# Copia o arquivo app.py para o contêiner
COPY app.py /app/app.py

# Define o diretório de trabalho
WORKDIR /app

# Comando para rodar o app quando o contêiner iniciar
CMD ["python3", "app.py"]
