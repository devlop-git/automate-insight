import json

from fastapi import Depends

from app.clients.insight_script import generate_insight_with_gemini,build_dashboard_insight
from app.clients.superset_client import SupersetClient
from app.dependencies.superset import get_superset_client
from app.models.chart import Chart
from app.models.dashboard import Dashboard
from app.repository.chart_insight_repository import ChartInsightRepository
from app.repository.chart_repository import ChartRepository
from app.repository.dashboard_repository import DashboardRepository
from app.schema.chart_schema import ChartResponse

# client = SupersetClient()
client:SupersetClient = Depends(get_superset_client)

class ChartService:
    def __init__(self):
        self.chartRepo = ChartRepository()
        self.chartInsightRepo = ChartInsightRepository()
        self.dashboardRepo = DashboardRepository()

    def create_chart(self, db, charts):
        return self.chartRepo.create_chart(db, charts)

    def get_all_charts(self, db, dashboard_id):
        return self.chartRepo.get_all_charts(db, dashboard_id)

    def get_chart_by_id(self, db, chart_id):
        chart = self.chartRepo.get_chart_by_id(db, chart_id)
        chart_dict = chart.__dict__
        chart_dict.pop("_sa_instance_state", None)
        # chart_dict = ChartResponse.model_validate(chart)
        # print("chart_dict", chart_dict)
        data = client.chartDetails_v1(chart_dict)
       
        return  self.generate_insights(db, data)
       
    
    def generate_insights(self, db, data):
        chart_payload = {
            "chart_id": data["chart_id"],
            "chart_name": data["chart_name"],
            "query_context": data["data"],
        }
        
        insights =  generate_insight_with_gemini(chart_payload)
        self.chartInsightRepo.create_chart_insight(db,insights)
        return insights
        

    def update_chart_data(self, db, charts):
        # chart_details = []
        chart_list = [
            {k: v for k, v in chart.__dict__.items() if not k.startswith("_")}
            for chart in charts
        ]
        for chart in chart_list:
            query_context = client.explore_v1(chart)
            update_data = {"query_context": query_context}
            self.chartRepo.update_query_context(
                db, chart_id=chart["chart_id"], data=update_data
            )
            # chart_details.append(client.chartDetails(chartInfo, query_context))

        return chart_list
    
    def get_all_charts_insights(self, db, dashboard_id):
        chart_insight = self.chartInsightRepo.get_all_chart_insight(db, dashboard_id)
        dashboard_insight = build_dashboard_insight(chart_insight)
        self.dashboardRepo.update_dashboard_insight(db,dashboard_insight,dashboard_id)
        return dashboard_insight
    
    