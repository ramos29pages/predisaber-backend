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
    archivo: str  # Ahora esperamos la ruta temporal del archivo


class ModeloPrediccionOut(ModeloPrediccionBase):
    id: str
    file_id: Optional[str] = None  # Solo necesitamos la referencia a GridFS

    class Config:
        orm_mode = True