from pydantic import BaseModel, EmailStr

class UsuarioBase(BaseModel):
    name: str
    email: EmailStr
    role : str
    semester : str
    identificacion: str
    tipo_prueba: str
    
class UsuarioCreate(UsuarioBase):
    picture: str
    

class UsuarioOut(UsuarioBase):
    id: str
    picture: str
    

    class Config:
        orm_mode = True