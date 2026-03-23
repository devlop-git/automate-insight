from app.repository.dashboard_repository import DashboardRepository


class DashboardService:
    def __init__(self):
        self.dashboardRepo = DashboardRepository()
        
    def create_dashboard(self,db,dashboard ):
        return self.dashboardRepo.create_dashboard(db,dashboard)
    
    def get_dashboards(self ):
        return self.dashboardRepo.get_dashboards()
    
    def get_dashboard_by_id(self , dashboard_id ):
        return self.dashboardRepo.get_dashboard_by_id(dashboard_id)