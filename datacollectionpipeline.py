import datetime as dt
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from my_functions import get_iss_data, insert_iss_data_into_db

default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2022, 1, 1),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5)
}

dag = DAG(
    'iss_data_collection',
    default_args=default_args,
    schedule_interval=dt.timedelta(minutes=30)
)

get_data_task = PythonOperator(
    task_id='get_iss_data',
    python_callable=get_iss_data,
    dag=dag
)

insert_data_task = PythonOperator(
    task_id='insert_iss_data_into_db',
    python_callable=insert_iss_data_into_db,
    dag=dag
)

create_table_task = MySqlOperator(
    task_id='create_table_iss_data',
    mysql_conn_id='my_mysql_connection',
    sql='''CREATE TABLE IF NOT EXISTS iss_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp TIMESTAMP,
                latitude FLOAT,
                longitude FLOAT,
                velocity FLOAT,
                altitude FLOAT
        );''',
    dag=dag
)

insert_data_task = MySqlOperator(
    task_id='insert_iss_data_into_db',
    mysql_conn_id='my_mysql_connection',
    sql='''INSERT INTO iss_data (timestamp, latitude, longitude, velocity, altitude)
                SELECT timestamp, latitude, longitude, velocity, altitude FROM iss_data_raw;
        ''',
    dag=dag
)

create_table_task >> get_data_task >> insert_data_task
