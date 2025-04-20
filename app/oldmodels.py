from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import datetime

# Esquemas para Usuario
class UsuarioBase(BaseModel):
    name: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioOut(UsuarioBase):
    id: str

    class Config:
        orm_mode = True

# Esquemas para Modelo de Predicción
class ModeloPrediccionBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    version: str
    tipo_prueba: str  # Por ejemplo, el tipo de prueba asociado al modelo

class ModeloPrediccionCreate(ModeloPrediccionBase):
    # En este caso se usará la subida de archivo por endpoint, por lo que aquí se puede omitir el archivo.
    pass

class ModeloPrediccionOut(ModeloPrediccionBase):
    id: str
    archivo: str  # Ruta o identificador del archivo almacenado

    class Config:
        orm_mode = True

# Esquemas para Prueba
class PruebaBase(BaseModel):
    nombre: str
    datos: str  # Se puede esperar un JSON serializado como string, o utilizar un campo dict si se prefiere

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
