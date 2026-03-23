from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.dependencies.superset import get_superset_client
from app.scripts.automate_insight import automate_insight
from app.services.chart_service import ChartService
from app.services.dashboard_service import DashboardService
from app.clients.superset_client import SupersetClient

router = APIRouter(prefix="/charts", tags=["charts"])
service = ChartService()
# client = SupersetClient()

class ChartController:
# @router.post("/")
    def create_chart( self,db: Session = Depends(get_db),client: SupersetClient = Depends(get_superset_client)):
        data = client.getChartList(id=210)
        
        return service.create_chart(db,data)
    
    def get_charts(self,db: Session = Depends(get_db)):
        charts = service.get_all_charts(db,210)
        
        # return service.update_chart_data(db,charts)
        return charts


    def generate_insights(self,db: Session = Depends(get_db)):
        charts = service.get_chart_by_id(db,1082)
        return charts

    def generate_dashboard_insights(self,db: Session = Depends(get_db)):
        return service.get_all_charts_insights(db,210)
    
    def automate_insight(self,dashboard_id):
        return automate_insight(dashboard_id)
    