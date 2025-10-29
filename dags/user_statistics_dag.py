"""
Daily User Statistics DAG

This DAG runs daily to calculate and log user statistics:
- Total number of users
- Average age
- Age range (min/max)
- Eye color distribution
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

# Add project root to path so we can import web_boilerplate
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web_boilerplate.airflow_helpers import run_user_statistics_sync


def calculate_user_statistics(**context):
    """Task function to calculate user statistics"""
    print("Starting user statistics calculation...")
    
    try:
        stats = run_user_statistics_sync()
        
        # Log results
        print(f"User Statistics calculated at {stats['calculated_at']}")
        print(f"Total users: {stats['total_users']}")
        print(f"Average age: {stats['average_age']}")
        print(f"Age range: {stats['min_age']} - {stats['max_age']}")
        print(f"Eye color distribution: {stats['eye_color_distribution']}")
        
        # Store in XCom for downstream tasks if needed
        context['ti'].xcom_push(key='user_statistics', value=stats)
        
        return stats
    except Exception as e:
        print(f"Error calculating user statistics: {str(e)}")
        raise


# Default arguments for the DAG
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
}

# Define the DAG
dag = DAG(
    'daily_user_statistics',
    default_args=default_args,
    description='Calculate and log daily user statistics',
    schedule_interval='0 1 * * *',  # Run daily at 1 AM UTC
    catchup=False,  # Don't run for past dates
    tags=['users', 'statistics', 'daily'],
)

# Define the task
calculate_stats_task = PythonOperator(
    task_id='calculate_user_statistics',
    python_callable=calculate_user_statistics,
    dag=dag,
)

# Task has no dependencies, so it's standalone
# If you add more tasks later, chain them like:
# task1 >> task2 >> task3

