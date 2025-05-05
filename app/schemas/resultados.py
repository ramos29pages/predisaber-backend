# 1. app/schemas/resultados.py
from pydantic import BaseModel, Field
from typing import List, Optional

class ResponseItem(BaseModel):
    question: str
    response: str

class ResultadoBase(BaseModel):
    user_id: str
    form_id: str
    asigned_id: str
    asigned_by: str
    completed_at: str
    prediction: float
    responses: List[ResponseItem]

class ResultadoCreate(ResultadoBase):
    # No incluir id: MongoDB lo genera
    pass

class ResultadoOut(ResultadoBase):
    id: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True