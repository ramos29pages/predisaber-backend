from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
import app.crud.usuarios as crud_usuarios
from app.schemas.usuarios import UsuarioCreate, UsuarioBase, UsuarioOut, UsuarioUpdate
from fastapi.responses import JSONResponse

router = APIRouter()

class PictureUpdate(BaseModel):
    picture: str  # URL de la imagen

@router.get("", response_model=list[UsuarioOut])
async def read_usuarios(skip: int = 0, limit: int = 100):
    return await crud_usuarios.get_usuarios(skip, limit)


@router.get("/{id}", response_model=UsuarioOut)
async def read_usuario(id: str):
    usuario = await crud_usuarios.get_usuario_by_id(id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario con ese ID no encontrado."
        )
    return usuario

@router.get("/email/{email}", response_model=UsuarioOut)
async def read_usuario(email: str):
    usuario = await crud_usuarios.get_usuario_by_email(email)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario con ese email no encontrado."
        )
    return usuario



@router.post("", response_model=UsuarioOut)
async def create_usuario(usuario: UsuarioCreate):
    existe = await crud_usuarios.get_usuario_by_email(usuario.email)
    if existe:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya existe.")
    nuevo_usuario = await crud_usuarios.create_usuario(usuario)
    return nuevo_usuario

@router.put("/{usuario_id}", response_model=UsuarioOut)
async def update_usuario(usuario_id: str, usuario: UsuarioUpdate):
    usuario_existente = await crud_usuarios.update_usuario(usuario_id, usuario)
    if not usuario_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario_existente

@router.delete("/{usuario_id}", response_model=UsuarioOut)
async def delete_usuario(usuario_id: str):
    usuario_eliminado = await crud_usuarios.delete_usuario(usuario_id)
    if not usuario_eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario_eliminado


@router.put("/email/{email}/picture", response_model=UsuarioOut)
async def update_picture_by_email(
    email: EmailStr,
    data: PictureUpdate
):
    # 1) Obtengo el dict bruto del usuario
    usuario = await crud_usuarios.get_usuario_by_email(email)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    usuario_id = usuario.get("id") or usuario.get("_id")

    # 2) Sólo creo el Pydantic con el campo que quiero cambiar
    update_obj = UsuarioUpdate(picture=data.picture)

    # 3) Llamo al CRUD que excluye unset y none
    usuario_actualizado = await crud_usuarios.update_usuario_picture(usuario_id, update_obj)
    if not usuario_actualizado:
        raise HTTPException(status_code=500, detail="No se pudo actualizar la imagen.")
    return usuario_actualizado