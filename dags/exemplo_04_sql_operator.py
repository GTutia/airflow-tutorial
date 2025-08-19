from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime

with DAG(
    dag_id = "exemplo_4_sql_operator",
    start_date=datetime(2025, 8, 17),
    schedule_interval="*/5 * * * *",
    tags = ['API','Postgres'],
    catchup = False
) as dag:

    run_sql_query = SQLExecuteQueryOperator(
        task_id="run_sql_query",
        conn_id="postgres_default",
        sql="""
            DROP TABLE IF EXISTS public.station_fact;
            CREATE TABLE public.station_fact AS (
                SELECT *
                FROM public.citybikes_log cl 
                WHERE updated_at = (SELECT MAX(updated_at) FROM public.citybikes_log)
            );
        """
    )
