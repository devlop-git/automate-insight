from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.dependencies.superset import get_superset_client
from app.services.dashboard_service import DashboardService
from app.clients.superset_client import SupersetClient

router = APIRouter(prefix="/dashboards", tags=["dashboards"])
service = DashboardService()
# client = SupersetClient()

class DashboardController:
# @router.post("/")
    def create_dashboard(self, db: Session = Depends(get_db),client: SupersetClient = Depends(get_superset_client)):
        data = client.getDashboardInfo(id=210)
        dashboard_data = {
            "name": data["dashboard_title"],
            "dashboard_id": data["id"]
        }
        return dashboard_data
        # return service.create_dashboard(db,dashboard_data)

