# Treinamento de Airflow

1. Clone o repositório numa pasta de sua escolha
2. Com o WSL e Docker Engine instalado, rode o comando docker compose up (ou sudo docker compose up)
3. Espere alguns minutos e acesse a interface do airflow em localhost:8081 e logue no airflow com usuário = airflow e senha = airflow
4. Com a interface do Airflow no ar, antes de ligar as DAGs, conecte ao banco local criado via DBeaver. port: 5433, user: postgres, password: postgres, host: localhost, banco de dados (dbname): citybik
5. Rode o comando abaixo para criar a tabela
6. Trige a DAG de exemplo 01

```
CREATE TABLE IF NOT EXISTS public.citybik_log (
    id TEXT not NULL,
    updated_at TIMESTAMPTZ,
    station_name TEXT NOT NULL,
    free_bikes INT NOT NULL,
    empty_slots INT NOT NULL,
    address TEXT null,
    distance_to_supersim FLOAT NULL,
    renting INT NOT NULL,
    "returning" INT NOT NULL,
    has_ebikes BOOLEAN NOT NULL,
    ebikes INT NOT NULL,
    normal_bikes INT NOT NULL,
    payment_terminal TEXT null,
    PRIMARY KEY (id, updated_at)
);
```
