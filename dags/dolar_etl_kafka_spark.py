from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'dolar_etl_kafka_spark',
    default_args=default_args,
    description='ETL con Kafka y Spark',
    schedule_interval='@hourly',
    start_date=datetime(2024, 12, 25),
    catchup=False,
) as dag:

    def start_kafka_producer():
        try:
            subprocess.run(["python", "/opt/airflow/scripts/kafka_producer.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error ejecutando el productor de Kafka: {e}")
            raise

    kafka_task = PythonOperator(
        task_id='start_kafka_producer',
        python_callable=start_kafka_producer,
    )

    spark_task = SparkSubmitOperator(
        task_id='process_with_spark',
        application="/opt/airflow/scripts/spark_processor.py",
        conn_id="spark_default"
    )

    kafka_task >> spark_task
