import time
import httpx
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()
last_pull = {"time": None, "count": 0, "status": "never run"}

@app.get("/")
def root():
    return {
        "message": "Job listing ingestion API — Acdyon Technologies assessment",
        "endpoints": {
            "/jobs": "Pulls latest job listings from RemoteOK",
            "/status": "Shows last pull time, count, and status"
        }
    }

def fetch_jobs():
    headers = {"User-Agent": "Mozilla/5.0 (compatible; JobBot/1.0)"}
    resp = httpx.get("https://remoteok.com/api", headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return [job for job in data if isinstance(job, dict) and job.get("id")]

def fetch_jobs_with_retry(max_retries=3):
    for attempt in range(max_retries):
        try:
            jobs = fetch_jobs()
            if jobs:
                return jobs
            raise ValueError("Empty response")
        except Exception as e:
            wait = 2 ** attempt
            print(f"Attempt {attempt+1} failed: {e}. Retrying in {wait}s")
            time.sleep(wait)
    return []

@app.get("/jobs")
def get_jobs():
    jobs = fetch_jobs_with_retry()
    last_pull.update(time=datetime.utcnow().isoformat(), count=len(jobs), status="ok" if jobs else "failed")
    return {"count": len(jobs), "jobs": jobs[:20]}

@app.get("/status")
def status():
    return last_pull