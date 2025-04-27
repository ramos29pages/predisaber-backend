import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Form
import os
import joblib
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

def unique_filename(filename: str) -> str:
    """Añade un UUID al nombre para evitar colisiones :contentReference[oaicite:2]{index=2}."""
    uid = uuid.uuid4().hex
    base, ext = os.path.splitext(filename)
    return f"{base}_{uid}.joblib"

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
    # Leer una sola vez
    contenido = await archivo.read()
    if not archivo.filename.endswith((".p", ".pickle")):
        raise HTTPException(400, "Extensión no permitida")

    tmp_path = os.path.join(UPLOAD_DIR, unique_filename(archivo.filename))
    # Escribir el contenido leído
    async with aiofiles.open(tmp_path, "wb") as out:
        await out.write(contenido)

    # Ahora tmp_path contiene datos; convertir a joblib
    model = joblib.load(tmp_path)    # OK: fichero no vacío :contentReference[oaicite:3]{index=3}
    joblib.dump(model, tmp_path)      # Serializa seguro como .joblib :contentReference[oaicite:4]{index=4}


    modelo_in = ModeloPrediccionCreate(
        nombre=nombre, creado_por=creado_por, precision=precision,
        date=date, descripcion=descripcion, version=version,
        variables=variables, archivo=tmp_path
    )
    try:
        return await create_modelo(modelo_in)
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))


# editar modelo
@router.put("/{modelo_id}", response_model=ModeloPrediccionOut, status_code=status.HTTP_202_ACCEPTED)
async def editar_modelo(
    modelo_id: str,
    nombre: str | None = Form(None),
    precision: float | None = Form(None),
    creado_por: str | None = Form(None),
    date: str | None = Form(None),
    descripcion: str | None = Form(None),
    version: float | None = Form(None),
    variables: list[str] | None = Form(None),
    archivo: UploadFile | None = File(None),
):
    
    if not ObjectId.is_valid(modelo_id):
        raise HTTPException(400, "ID inválido")

    update_data: dict = {}
    if nombre      is not None: update_data["nombre"]      = nombre
    if precision   is not None: update_data["precision"]   = precision
    if creado_por  is not None: update_data["creado_por"]  = creado_por
    if date        is not None: update_data["date"]        = date
    if descripcion is not None: update_data["descripcion"] = descripcion
    if version     is not None: update_data["version"]     = version
    if variables   is not None: update_data["variables"]   = variables

    tmp_path = ""
    if archivo:
        # repetir lógica de guardado único
        contenido = await archivo.read()
        await archivo.seek(0)
        tmp_path = os.path.join(UPLOAD_DIR, unique_filename(archivo.filename))
        async with aiofiles.open(tmp_path,"wb") as out:
            await out.write(contenido)
        m = joblib.load(tmp_path)
        joblib.dump(m, tmp_path)
        update_data["archivo"] = tmp_path

    # modelo_in = ModeloPrediccionCreate(
    #     nombre=nombre, creado_por=creado_por,
    #     precision=precision, date=date,
    #     descripcion=descripcion, version=version,
    #     variables=variables, archivo=tmp_path or None
    # )
    try:
        return await update_modelo(modelo_id, update_data)
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e))
    
    

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

@router.delete("/{modelo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_modelo(modelo_id: str):
    if not ObjectId.is_valid(modelo_id):
        raise HTTPException(400, "ID inválido")
    success = await delete_modelo(modelo_id)
    if not success:
        raise HTTPException(404, "No encontrado")