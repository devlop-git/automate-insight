from sqlalchemy import Column, Integer, Text, ForeignKey, DECIMAL, JSON
from sqlalchemy.orm import relationship
from app.core.base import BaseModel

class ChartInsight(BaseModel):
    __tablename__ = "chart_insights"

    id = Column(Integer, primary_key=True, index=True)
    chart_id = Column(Integer, ForeignKey("charts.chart_id"))
    insight_text = Column(Text)
    confidence_score = Column(DECIMAL(3,2))
    usage_metadata = Column(JSON)

    chart = relationship("Chart")