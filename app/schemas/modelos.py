from pydantic import BaseModel
from typing import Optional

class ModeloPrediccionBase(BaseModel):
    nombre: str
    precision: int
    descripcion: Optional[str] = None
    version: str
    tipo_prueba: str

class ModeloPrediccionCreate(ModeloPrediccionBase):
    archivo: str  # ruta donde se guardará el pickle

class ModeloPrediccionOut(ModeloPrediccionBase):
    id: str
    archivo: str

    class Config:
        orm_mode = True
