from app.models.chart import Chart


class ChartRepository:
    
    def create_chart(self,db,charts ):
        db_chart = [Chart(**chart) for chart in charts]
        db.add_all(db_chart)
        db.commit()
        return db_chart
    
    def get_all_charts(self,db,dashboard_id):
        return db.query(Chart).filter(Chart.dashboard_id == dashboard_id).all()
    
    def get_chart_by_id(self,db,chart_id):
        return db.query(Chart).filter(Chart.chart_id == chart_id).first()
    
    def update_query_context(self, db, chart_id, data):
        
        db.query(Chart).filter(
            Chart.chart_id == chart_id
        ).update(data)

        db.commit()