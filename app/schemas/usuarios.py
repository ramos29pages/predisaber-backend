from typing import Optional
from pydantic import BaseModel, EmailStr

class UsuarioBase(BaseModel):
    name: str
    email: EmailStr
    role : str
    semester : int
    identificacion: int
    tipo_prueba: str
    
class UsuarioCreate(UsuarioBase):
    picture: str

class UsuarioUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    semester: Optional[int] = None
    identificacion: Optional[int] = None
    tipo_prueba: Optional[str] = None
    picture: Optional[str] = None

class UsuarioOut(UsuarioBase):
    id: str
    picture: str
    

    class Config:
        orm_mode = True