from fastapi import APIRouter
from app.clients.superset_client import SupersetClient
from app.clients.insight_script import bulid_dashboard_insight, generate_all_insights

router = APIRouter()

client = SupersetClient()

@router.get("/dashboard/{id}")
def dashboard(id: int):
    chart_details = []
    charts = client.getChartList(id)
    charts = charts[:5]
    for chart in charts:
        sliceInfo, query_context = client.explore(chart)
        chart_details.append(client.chartDetails(sliceInfo, query_context))
    results = generate_all_insights(chart_details)
    return {"data": results}