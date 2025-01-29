# Gerenciador de Tarefas - Arquitetura Baseada em Cloud Run

# Visão Geral

Este projeto demonstra a implementação de um Gerenciador de Tarefas utilizando Python, com uma arquitetura moderna baseada em containers e serviços gerenciados do Google Cloud Platform (GCP). O objetivo principal não é apenas a funcionalidade da aplicação, mas sim destacar como uma abordagem baseada em Cloud Run e Cloud SQL pode proporcionar escalabilidade, disponibilidade e eficiência operacional para aplicações empresariais.

# Motivação e Benefícios para Negócios

Com a adoção de Cloud Run e Cloud SQL, esta solução exemplifica como empresas podem:

Reduzir custos operacionais ao eliminar a necessidade de gerenciar infraestrutura física ou VMs.

Aumentar a escalabilidade com a capacidade de ajuste automático de instâncias conforme a demanda.

Garantir alta disponibilidade utilizando um banco de dados gerenciado e um serviço de execução de containers serverless.

Melhorar a segurança ao utilizar autenticação integrada entre serviços do GCP e evitar exposição desnecessária de dados.

# Arquitetura da Solução

Desenvolvimento e Testes Locais: O Gerenciador de Tarefas foi desenvolvido em Python e testado localmente, conectado a uma instância do Cloud SQL (PostgreSQL).

Containerização: A aplicação foi empacotada em um container Docker, garantindo portabilidade e consistência entre ambientes.

Armazenamento da Imagem: A imagem Docker foi enviada para o Artifact Registry do GCP, permitindo versionamento e controle seguro do deployment.

Deploy no Cloud Run: A aplicação foi implantada no Cloud Run, um serviço serverless que permite escalabilidade automática sem necessidade de gerenciamento de infraestrutura.

# Fluxo de Implementação

### 1. Construção e Testes Locais

Desenvolvimento em Python e conexão com Cloud SQL.

Testes e validação da aplicação localmente.

# 2. Construção da Imagem Docker

#Criar imagem Docker
docker build -t gcr.io/<meu-projeto>/gerenciador-tarefas:latest .

# 3. Envio para o Artifact Registry

#Autenticação no GCP
gcloud auth configure-docker

#Enviar imagem para o Artifact Registry
docker push gcr.io/<meu-projeto>/gerenciador-tarefas:latest

# 4. Deploy no Cloud Run

# Implantar aplicação no Cloud Run
 gcloud run deploy gerenciador-tarefas \
    --image=gcr.io/<meu-projeto>/gerenciador-tarefas:latest \
    --platform=managed \
    --region=<regiao> \
    --allow-unauthenticated \
    --add-cloudsql-instances=<minha-instancia-cloudsql>

# Considerações Finais

Este projeto serve como um exemplo prático de como aplicações podem ser modernizadas utilizando serviços gerenciados na nuvem. Empresas que adotam essa abordagem podem otimizar custos, melhorar a segurança e escalar suas aplicações de maneira eficiente.

A ideia central aqui não é apenas um gerenciador de tarefas, mas sim demonstrar habilidades em computação em nuvem, DevOps e arquitetura serverless, tornando-se um diferencial para profissionais que desejam atuar na área de Cloud Computing e DevOps.

