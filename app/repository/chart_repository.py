from app.models.chart import Chart
from sqlalchemy.dialects.postgresql import insert

class ChartRepository:
    
    def create_chart(self,db,charts ):
        stmt = insert(Chart).values(charts)

        stmt = stmt.on_conflict_do_nothing(
            index_elements=["chart_id"]   # unique column
        )

        db.execute(stmt)
        db.commit()

        return charts
    def get_all_charts(self,db,dashboard_id):
        return db.query(Chart).filter(Chart.dashboard_id == dashboard_id).all()
    
    def get_chart_by_id(self,db,chart_id):
        return db.query(Chart).filter(Chart.chart_id == chart_id).first()
    
    def update_query_context(self, db, chart_id, data):
        
        db.query(Chart).filter(
            Chart.chart_id == chart_id
        ).update(data)

        db.commit()