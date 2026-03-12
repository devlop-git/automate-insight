from fastapi import FastAPI
from app.routes.dashboard_routes import router

app = FastAPI(
    title="Superset AI Insights API",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/health")
def healthCheck():
    return {"status": "ok"}