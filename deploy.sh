#!/bin/bash

# Copiar arquivos da aplicação para a VM
gcloud compute scp --recurse * python-app:/home/$USER/app/

# Reiniciar o serviço da aplicação na VM
gcloud compute ssh python-app --command "
sudo pkill gunicorn || true;
cd /home/$USER/app;
gunicorn -b 0.0.0.0:5000 app:app --daemon;
"
