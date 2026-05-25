import json
import csv
from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
import requests

def fetch_jobs():
    url = "https://remotive.com/api/remote-jobs"
    response = requests.get(url)
    data = response.json()
    with open("/tmp/jobs.json", "w") as f:
        json.dump(data, f)
    print(f"Total jobs fetched: {len(data['jobs'])}")

def filter_jobs():
    with open("/tmp/jobs.json", "r") as f:
        data = json.load(f)
    jobs = data["jobs"]
    KEYWORDS = ["data", "engineer", "analyst", "customer", "support", "warehouse", "psw"]
    filtered = []
    for job in jobs:
        title = job["title"].encode("utf-8", "ignore").decode("utf-8").lower()
        for keyword in KEYWORDS:
            if keyword in title:
                filtered.append(job)
                break
    print(f"Filtered jobs: {len(filtered)}")
    with open('/tmp/filtered_jobs.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Company", "URL"])
        for job in filtered:
            writer.writerow([job["title"], job["company_name"], job["url"]])
    print("Filtered jobs saved to /tmp/filtered_jobs.csv")

with DAG(
    dag_id="job_tracker_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    fetch_jobs_task = PythonOperator(
        task_id="fetch_jobs",
        python_callable=fetch_jobs
    )

    filter_jobs_task = PythonOperator(
        task_id="filter_jobs",
        python_callable=filter_jobs
    )

    fetch_jobs_task >> filter_jobs_task
