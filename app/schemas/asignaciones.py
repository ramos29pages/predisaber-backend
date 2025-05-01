from pydantic import BaseModel
from typing import Optional

class AsignacionBase(BaseModel):
    user_id: str
    form_id: str
    created_at: str  # Requerido en la creación según el modelo dado

class AsignacionCreate(AsignacionBase):
    pass  # Utiliza los campos de AsignacionBase

class AsignacionOut(AsignacionBase):
    id: str  # Campo adicional para respuestas
    
    class Config:
        orm_mode = True  # Permite trabajar con objetos ORM [[8]]