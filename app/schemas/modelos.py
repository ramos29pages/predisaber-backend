from pydantic import BaseModel
from typing import Optional

class ModeloPrediccionBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    version: str
    tipo_prueba: str

class ModeloPrediccionCreate(ModeloPrediccionBase):
    pass

class ModeloPrediccionOut(ModeloPrediccionBase):
    id: str
    archivo: str

    class Config:
        orm_mode = True