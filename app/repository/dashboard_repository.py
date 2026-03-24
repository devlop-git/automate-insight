from fastapi import Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.models.dashboard import Dashboard
from sqlalchemy.dialects.postgresql import insert

class DashboardRepository():
   
    def create_dashboard(self,db,dashboard ):
        db_dashboard = Dashboard(**dashboard)
        db.add(db_dashboard)
        db.commit()
        db.refresh(db_dashboard)
        return db_dashboard
    
    def create_all_dashboard(self,db,dashboards ):
        stmt = insert(Dashboard).values(dashboards)

        stmt = stmt.on_conflict_do_nothing(
            index_elements=["dashboard_id"]   # unique column
        )

        db.execute(stmt)
        db.commit()
        
        return dashboards
        
    def get_all_dashboards(self,db ):
        return db.query(Dashboard).all()
    
    def get_dashboard_by_id(self , dashboard_id ):
        pass    
    
    def update_dashboard_insight(self,db,update_data,dashboard_id):
        db.query(Dashboard).filter(Dashboard.dashboard_id == dashboard_id).update(update_data)
        db.commit()