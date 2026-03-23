from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.base import BaseModel

class LLMLog(BaseModel):
    __tablename__ = "llm_logs"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer)
    dashboard_id = Column(Integer, ForeignKey("dashboards.id"))
    chart_id = Column(Integer, ForeignKey("charts.id"))
    prompt = Column(Text)
    response = Column(Text)

    dashboard = relationship("Dashboard")
    chart = relationship("Chart")