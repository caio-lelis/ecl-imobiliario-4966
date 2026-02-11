# Ambiente de Orquestração e ML Tracking com Docker

## Este projeto sobe um ambiente integrado com:

- Postgres (banco de dados)
- Airflow (orquestração de workflows)
- MLflow (rastreamento de experimentos de Machine Learning)
- Pré-requisitos
- Docker instalado
- Docker Compose disponível (docker compose ou docker-compose)
  Verifique versões: bash docker --version docker compose version

## Subindo os serviços

Inicie o banco Postgres: bash docker compose up -d postgres

## Crie o banco para o MLflow:

docker exec -it postgres psql -U airflow -d airflow -c "CREATE DATABASE mlflow;"

## Inicialize o banco do Airflow: bash docker compose run --rm airflow-webserver airflow db init

## Crie o usuário admin padrão no Airflow:

docker compose run --rm airflow-webserver airflow users create
--username admin
--firstname Admin
--lastname User
--role Admin
--email admin@example.com
--password admin

## Suba todos os serviços:

docker compose up -d

### Acessando as aplicações

### Airflow Web UI:

- http://localhost:8080
- Usuário: admin
- Senha: admin

### MLflow Tracking UI:

- http://localhost:5000
- Postgres: porta 5432
- Usuário: airflow
- Senha: airflow

### Comandos úteis

Parar os serviços:

docker compose down

Ver logs:

docker compose logs -f

Reiniciar:

docker compose restart

### Observações

A chave Fernet usada pelo Airflow deve ser válida. Para gerar uma nova: bash python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
Atualize o valor em docker-compose.yml na variável AIRFLOW**CORE**FERNET_KEY.

Os DAGs devem ser colocados na pasta dags para serem reconhecidos pelo Airflow.
