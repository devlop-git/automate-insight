from app.models.chart import Chart
from app.models.chart_insight import ChartInsight


class ChartInsightRepository:

    def create_chart_insight(self, db, chart_insights):
        db_chart_insight = ChartInsight(**chart_insights)
        db.add(db_chart_insight)
        db.commit()
        db.refresh(db_chart_insight)
        return db_chart_insight

    def get_all_chart_insight(self, db, dashboard_id):
        return (
            db.query(Chart.chart_name, ChartInsight.insight_text)
            .join(ChartInsight, Chart.chart_id == ChartInsight.chart_id)
            .filter(Chart.dashboard_id == dashboard_id)
            .all()
        )
