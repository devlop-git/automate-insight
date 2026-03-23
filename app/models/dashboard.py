from sqlalchemy import Column, Integer, String, JSON
from app.core.base import BaseModel

class Dashboard(BaseModel):
    __tablename__ = "dashboards"

    id=Column(Integer, primary_key=True, index=True)
    dashboard_id = Column(Integer, unique=True)
    name = Column(String(255))
    insight = Column(JSON)
    usage_metadata = Column(JSON)