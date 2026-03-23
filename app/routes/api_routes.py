from fastapi import APIRouter
import app.api as controller

chartController = controller.ChartController()
dashboardController = controller.DashboardController()

router = APIRouter(prefix="/api", tags=["api"])

# @router.post("/")
@router.get("/health_check")
def health_check():
    return {"status": "ok"} 

router.add_api_route("/dashboard", dashboardController.create_dashboard, methods=["POST"])
router.add_api_route("/charts", chartController.create_chart, methods=["POST"])
router.add_api_route("/charts", chartController.get_charts, methods=["GET"])
router.add_api_route("/insights", chartController.generate_insights, methods=["GET"])
router.add_api_route("/dashboard_insights", chartController.generate_dashboard_insights, methods=["GET"])

router.add_api_route("/automate_insight/{dashboard_id}", chartController.automate_insight, methods=["GET"])