from fastapi import FastAPI
from app.routers import assessment_router
from datetime import datetime

app = FastAPI(title="Calfit API")

app.include_router(assessment_router.router)

@app.get("/")
def read_root():
    return {"message": "Calfit API is Running"}

@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}