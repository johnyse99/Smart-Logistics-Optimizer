from pydantic import BaseModel
from typing import List

class DemandPrediction(BaseModel):
    customer_id: int
    customer_name: str
    predicted_demand: float

class PredictionReport(BaseModel):
    day: int
    predictions: List[DemandPrediction]