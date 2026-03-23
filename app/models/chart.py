from app.core.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

class Chart(BaseModel):
    __tablename__ = "charts"

    id = Column(Integer, primary_key=True, index=True)
    dashboard_id = Column(Integer, ForeignKey("dashboards.dashboard_id"))
    chart_id = Column(Integer,unique=True)
    chart_name = Column(String(255))
    chart_url = Column(String(255))
    chart_type = Column(String(100))
    query_context = Column(JSONB)
    raw_data = Column(JSONB)
    dashboard = relationship("Dashboard")