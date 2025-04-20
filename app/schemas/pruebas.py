from pydantic import BaseModel
import datetime

class PruebaBase(BaseModel):
    nombre: str
    datos: str

class PruebaCreate(PruebaBase):
    usuario_id: str
    modelo_id: str

class PruebaOut(PruebaBase):
    id: str
    fecha: datetime.datetime
    usuario_id: str
    modelo_id: str

    class Config:
        orm_mode = True