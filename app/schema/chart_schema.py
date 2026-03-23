from app.core.base import BaseModel


from pydantic import BaseModel, ConfigDict

class ChartResponse(BaseModel):
    id: int
    chart_name: str
    chart_url : str
    chart_type : str | None
    query_context : dict | None

    model_config = ConfigDict(from_attributes=True)