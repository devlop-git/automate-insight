from app.models.chart import Chart
from app.models.chart_insight import ChartInsight
from sqlalchemy.dialects.postgresql import insert

class ChartInsightRepository:

    def create_chart_insight(self, db, chart_insights):
        db_chart_insight = ChartInsight(**chart_insights)
        db.add(db_chart_insight)
        db.commit()
        db.refresh(db_chart_insight)
        return db_chart_insight
    
    def upsert_chart_insights(db, chart_insight):

        stmt = insert(ChartInsight).values(chart_insight)

        stmt = stmt.on_conflict_do_update(
            index_elements=["chart_id"],   # unique column
            set_={
                "insight_text": stmt.excluded.insight_text,
                "confidence_score": stmt.excluded.confidence_score,
                "usage_metadata": stmt.excluded.usage_metadata,
            }
        )

        db.execute(stmt)
        db.commit()

    def get_all_chart_insight(self, db, dashboard_id):
        return (
            db.query(Chart.chart_name, ChartInsight.insight_text)
            .join(ChartInsight, Chart.chart_id == ChartInsight.chart_id)
            .filter(Chart.dashboard_id == dashboard_id)
            .all()
        )
