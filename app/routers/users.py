from fastapi import APIRouter, HTTPException, status
from app import models, crud
from app.models import UsuarioCreate, UsuarioBase, UsuarioOut
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/", response_model=list[UsuarioOut])
async def read_usuarios(skip: int = 0, limit: int = 100):
    return await crud.get_usuarios(skip, limit)

@router.post("/", response_model=UsuarioOut)
async def create_usuario(usuario: UsuarioCreate):
    existe = await crud.get_usuario_by_email(usuario.email)
    if existe:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya existe.")
    nuevo_usuario = await crud.create_usuario(usuario)
    return nuevo_usuario

@router.put("/{usuario_id}", response_model=UsuarioOut)
async def update_usuario(usuario_id: str, usuario: UsuarioBase):
    usuario_existente = await crud.update_usuario(usuario_id, usuario)
    if not usuario_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario_existente

@router.delete("/{usuario_id}", response_model=UsuarioOut)
async def delete_usuario(usuario_id: str):
    usuario_eliminado = await crud.delete_usuario(usuario_id)
    if not usuario_eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario_eliminado
