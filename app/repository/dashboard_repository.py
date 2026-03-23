from fastapi import Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.models.dashboard import Dashboard

class DashboardRepository():
   
    
    
    def create_dashboard(self,db,dashboard ):
        db_dashboard = Dashboard(**dashboard)
        db.add(db_dashboard)
        db.commit()
        db.refresh(db_dashboard)
        return db_dashboard
       
    def get_dashboards(self ):
        pass
    
    def get_dashboard_by_id(self , dashboard_id ):
        pass    
    
    def update_dashboard_insight(self,db,update_data,dashboard_id):
        db.query(Dashboard).filter(Dashboard.dashboard_id == dashboard_id).update(update_data)
        db.commit()