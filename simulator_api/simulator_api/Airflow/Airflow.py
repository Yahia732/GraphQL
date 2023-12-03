import json
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproject.settings")

# Initialize Django
django.setup()
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from simulator_api.models import *
from simulator_api.timeseries.simulator import simulate_simulator
from django.core.serializers import serialize


# Get all objects from the model
all_simulators = Simulator.objects.all()

for row in all_simulators:

    dag_id = f"dynamic_dag_{row['pk']}"  # Unique DAG ID for each row
    simulate_simulator(row.id)
    default_args = {
            'owner': 'airflow',
            'start_date': datetime(2023, 11, 14),
            # Add other args as needed
         }

    with DAG(dag_id=dag_id,
        default_args=default_args,
        schedule_interval=timedelta(days=row.interval),
        catchup=False) as dag:


        run_simulator = PythonOperator(
            task_id='create_dag_for_each_row',
            python_callable=simulate_simulator,
            op_args=[row['pk']],
            dag=dag)
        run_simulator

