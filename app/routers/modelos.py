from fastapi import APIRouter, UploadFile, File, HTTPException, status, Form
import os
from typing import Annotated
from app import controller
from app.schemas.modelos import ModeloPrediccionOut, ModeloPrediccionCreate
from app.crud.modelos import create_modelo, get_modelos
import shutil
import os, aiofiles
from bson import ObjectId
from app.schemas.modelos import ModeloPrediccionCreate, ModeloPrediccionOut
from app.crud.modelos import (
    create_modelo, get_modelos, get_modelo_by_id, get_modelos_by_name,
    list_model_names, list_versions_per_name, update_modelo, delete_modelo
)

router = APIRouter()

# Asegurarse de que exista el directorio para los archivos subidos
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=ModeloPrediccionOut, status_code=status.HTTP_201_CREATED)
async def registrar_modelo(
    nombre: str = Form(...),
    precision: str = Form(...),
    creado_por: str = Form(...),
    date: str = Form(...),
    descripcion: str | None = Form(None),
    version: str = Form(...),
    archivo: UploadFile = File(...),
    variables: list[str] = Form(...)
):
    contenido = await archivo.read()
    print(archivo, 'ARCHIVO')
    print(contenido, 'contenido')
    ext = os.path.splitext(archivo.filename)[1]
    if ext not in [".p", ".pickle"]:
        raise HTTPException(400, "Extensión no permitida")  # :contentReference[oaicite:5]{index=5}
    path = os.path.join(UPLOAD_DIR, archivo.filename)
    async with aiofiles.open(path, "wb") as out:
        await out.write(await archivo.read())  # 
    modelo_in = ModeloPrediccionCreate(
        nombre=nombre, creado_por=creado_por,
        precision=precision, date=date,
        descripcion=descripcion, version=version,
        variables=variables, archivo=path
    )
    return await create_modelo(modelo_in)

@router.get("/", response_model=list[ModeloPrediccionOut])
async def leer_modelos(skip: int = 0, limit: int = 100):
    return await get_modelos(skip, limit)

@router.get("/ids/{modelo_id}", response_model=ModeloPrediccionOut)
async def leer_modelo_id(modelo_id: str):
    if not ObjectId.is_valid(modelo_id):
        raise HTTPException(400, "ID inválido")
    m = await get_modelo_by_id(modelo_id)
    if not m:
        raise HTTPException(404, "No encontrado")
    return m

@router.get("/nombre/{nombre}", response_model=list[ModeloPrediccionOut])
async def leer_modelos_nombre(nombre: str):
    return await get_modelos_by_name(nombre)

@router.get("/nombres", response_model=list[str])
async def listar_nombres():
    return await list_model_names()

@router.get("/versiones", response_model=dict[str, list[str]])
async def listar_versiones():
    return await list_versions_per_name()

@router.put("/{modelo_id}", response_model=ModeloPrediccionOut)
async def editar_modelo(modelo_id: str, data: ModeloPrediccionCreate):
    if not ObjectId.is_valid(modelo_id):
        raise HTTPException(400, "ID inválido")
    updated = await update_modelo(modelo_id, data.dict())
    return updated

@router.delete("/{modelo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_modelo(modelo_id: str):
    if not ObjectId.is_valid(modelo_id):
        raise HTTPException(400, "ID inválido")
    success = await delete_modelo(modelo_id)
    if not success:
        raise HTTPException(404, "No encontrado")