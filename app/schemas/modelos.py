from pydantic import BaseModel, Field
from typing import Optional, List


class ModeloPrediccionBase(BaseModel):
    nombre: str
    creado_por: str
    precision: float
    date: str
    descripcion: Optional[str] = None
    version: float
    variables: List[str] = Field(default_factory=list)

class ModeloPrediccionCreate(ModeloPrediccionBase):
    archivo: str  # ruta donde se guardará el pickle

class ModeloPrediccionOut(ModeloPrediccionBase):
    id: str
    archivo: str

    class Config:
        orm_mode = True
