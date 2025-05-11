import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Form
import os
import joblib
from typing import Annotated, List
from app import controller
from app.crud.models.update import update_model
from app.schemas.modelos import ModeloPrediccionOut, ModeloPrediccionCreate
from app.crud.modelos import get_modelos
import shutil
import os, aiofiles
from bson import ObjectId
from app.schemas.modelos import ModeloPrediccionCreate, ModeloPrediccionOut
from app.crud.modelos import (
    get_modelos, get_modelo_by_id, get_modelos_by_name,
    list_model_names, list_versions_per_name, delete_modelo
)
from app.crud.models.create import create_model

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
    variables: List[str] = Form(...)
):
    if not archivo.filename.endswith((".p", ".pickle")):
        raise HTTPException(400, "Extensión no permitida")

    unique_file = unique_filename(archivo.filename)
    tmp_path = os.path.join(UPLOAD_DIR, unique_file)

    try:
        contenido = await archivo.read()
        async with aiofiles.open(tmp_path, "wb") as out:
            await out.write(contenido)

        # Cargar y volver a guardar con joblib (como en tu código)
        try:
            model = joblib.load(tmp_path)
            joblib.dump(model, tmp_path)
        except Exception as e:
            os.remove(tmp_path)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al procesar el archivo del modelo: {str(e)}")

        modelo_in = ModeloPrediccionCreate(
            nombre=nombre, creado_por=creado_por, precision=precision,
            date=date, descripcion=descripcion, version=version,
            variables=variables, archivo=tmp_path  # Pasar la ruta temporal
        )
        return await create_model(modelo_in)
    except HTTPException as e:
        raise e
    except Exception as e:
        # Asegúrate de limpiar el archivo temporal en caso de otros errores
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Error inesperado al registrar el modelo: {str(e)}")

# Función de utilidad para generar nombres de archivo únicos
def unique_filename(filename: str) -> str:
    name, ext = os.path.splitext(filename)
    return f"{name}_{uuid.uuid4()}{ext}"

# editar modelo
@router.put(
    "/{modelo_id}",
    response_model=ModeloPrediccionOut,
    status_code=status.HTTP_202_ACCEPTED
)
async def editar_modelo(
    modelo_id: str,
    nombre: str | None       = Form(None),
    precision: float | None  = Form(None),
    creado_por: str | None   = Form(None),
    date: str | None         = Form(None),
    descripcion: str | None  = Form(None),
    version: float | None    = Form(None),
    variables: list[str] | None = Form(None),
    archivo: UploadFile | None   = File(None),
):
    if not ObjectId.is_valid(modelo_id):
        raise HTTPException(400, "ID inválido")

    # 1) Preparamos el dict de actualización
    update_data: dict = {}
    if nombre      is not None: update_data["nombre"]      = nombre
    if precision   is not None: update_data["precision"]   = precision
    if creado_por  is not None: update_data["creado_por"]  = creado_por
    if date        is not None: update_data["date"]        = date
    if descripcion is not None: update_data["descripcion"] = descripcion
    if version     is not None: update_data["version"]     = version
    if variables   is not None: update_data["variables"]   = variables

    # 2) Si viene un nuevo archivo, lo guardamos temporalmente
    tmp_path: str | None = None
    if archivo:
        if not archivo.filename.endswith((".p", ".pickle")):
            raise HTTPException(400, "Extensión de archivo no permitida")
        unique_file = unique_filename(archivo.filename)
        tmp_path = os.path.join(UPLOAD_DIR, unique_file)

        contenido = await archivo.read()
        async with aiofiles.open(tmp_path, "wb") as out:
            await out.write(contenido)

        # Validamos que sea un pickle válido
        try:
            model_obj = joblib.load(tmp_path)
            joblib.dump(model_obj, tmp_path)
        except Exception as e:
            os.remove(tmp_path)
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Error al procesar el archivo del modelo: {e}"
            )
        # Marcamos en update_data que tenemos ruta temporal
        update_data["archivo"] = tmp_path

    # 3) Delegamos en la función CRUD
    try:
        nuevo = await update_model(modelo_id, update_data)
    finally:
        # Siempre limpiamos el temporal aunque haya fallado
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    return nuevo

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