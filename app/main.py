from fastapi import FastAPI
from app.routes.api_routes import router
from app.routes.dashboard_routes import router_v1
# from app.routes.dashboard_routes import router
# from app.api import dashboard_controller, chart_controller

app = FastAPI(
    title="Superset AI Insights API",
    version="1.0.0"
)

app.include_router(router)
# app.include_router(router_v1)

# app.include_router(dashboard_controller.router)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/health")
def healthCheck():
    return {"status": "ok"}