from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime, timedelta

TOPICO = "treinamento-airflow"

with DAG(
    dag_id = "exemplo_6_alerta",
    start_date=datetime(2025, 8, 17),
    schedule_interval="*/5 * * * *",
    tags = ['API','Postgres'],
    catchup = False
) as dag:

    get_bikes = SQLExecuteQueryOperator(
        task_id="get_bikes",
        conn_id="postgres_default",
        sql="""
            SELECT free_bikes
            FROM public.station_fact
            ORDER BY distance_to_supersim
            LIMIT 1;
        """,
    )

    notify = SimpleHttpOperator(
        task_id="publicar_no_site",
        http_conn_id="ntfy",
        endpoint=TOPICO,
        method="POST",
        headers={
            "Content-Type": "text/plain",
            "Title": "Tutorial de Airflow",
            "Priority": "4",
        },
        data="Temos {{ ti.xcom_pull('get_bikes')[0][0] | default('N/A') }} bicileta perto da SuperSim!",
    )

    get_bikes >> notify
