from fastapi import Depends

from app.clients.superset_client import SupersetClient
from app.dependencies.database import get_db
from app.dependencies.superset import get_superset_client
from app.repository.chart_repository import ChartRepository
from app.services.chart_service import ChartService
from app.services.dashboard_service import DashboardService
from sqlalchemy.orm import Session

chart_service = ChartService()
dashboard_service = DashboardService()
chartRepo = ChartRepository()


def automate_insight(dashboard_id):
    
    db = next(get_db())
    client = get_superset_client()
    
    # Import dashboard Info
    data = client.getDashboardInfo(dashboard_id)
    dashboard_data = {
        "name": data["dashboard_title"],
        "dashboard_id": data["id"]
    }
    dashboard_service.create_dashboard(db,dashboard_data)
    
    # Import charts
    charts = client.getChartList(dashboard_id)
    # for chart in charts:
    chart_service.create_chart(db,chart)
        
    # Import charts insights
    # charts = client.getChartList(dashboard_id)
    for chart in charts:    
        print(chart)
        # chart_service.get_chart_by_id(db,chart["id"])
        query_context = client.explore_v1(chart)
        update_data = {"query_context": query_context}
        chartRepo.update_query_context(db, chart_id=chart["chart_id"], data=update_data)
        chart["query_context"] = query_context
        data = client.chartDetails_v1(chart)
        chart_service.generate_insights(db,data)
        
    # Generate Dashboard Insight
    chart_service.get_all_charts_insights(db,dashboard_id)
        
    
        
    