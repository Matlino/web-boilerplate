# Airflow Setup Guide

## Installation

1. Install project dependencies (including Airflow):
```bash
poetry install
```

2. Initialize Airflow (first time only):
```bash
export AIRFLOW_HOME=$PWD/airflow
mkdir -p $AIRFLOW_HOME/dags
mkdir -p $AIRFLOW_HOME/logs
mkdir -p $AIRFLOW_HOME/plugins

# Initialize database
poetry run airflow db init

# Create admin user (replace with your credentials)
poetry run airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

## Configuration

Set these environment variables:
```bash
export AIRFLOW_HOME=$PWD/airflow
export AIRFLOW__CORE__DAGS_FOLDER=$PWD/dags
```

Or create `$AIRFLOW_HOME/airflow.cfg` and configure:
```ini
[core]
dags_folder = /path/to/web-boilerplate/dags
```

## Running Airflow

1. Start scheduler (in one terminal):
```bash
export AIRFLOW_HOME=$PWD/airflow
poetry run airflow scheduler
```

2. Start webserver (in another terminal):
```bash
export AIRFLOW_HOME=$PWD/airflow
poetry run airflow webserver --port 8080
```

3. Access Airflow UI:
   - Open browser: http://localhost:8080
   - Login with admin/admin (or credentials you created)
   - Find "daily_user_statistics" DAG
   - Enable and trigger it

## DAG Details

- **Name**: `daily_user_statistics`
- **Schedule**: Daily at 1 AM UTC (`0 1 * * *`)
- **Task**: Calculates user statistics:
  - Total users
  - Average age
  - Age range (min/max)
  - Eye color distribution

## Troubleshooting

1. **DAG not appearing**: Check logs, ensure DAGs folder is correct
2. **Import errors**: Make sure web_boilerplate is in Python path
3. **Database connection**: Check DATABASE_URL in .env file

