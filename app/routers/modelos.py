from fastapi import APIRouter, UploadFile, File, HTTPException, status, Form
import os
from app import controller
from app.schemas.modelos import ModeloPrediccionOut
from app.crud.modelos import create_modelo, get_modelos
import shutil
import aiofiles

router = APIRouter()

# Asegurarse de que exista el directorio para los archivos subidos
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=ModeloPrediccionOut)
async def registrar_modelo(
    nombre: str = Form(...),
    descripcion: str | None = Form(None),
    version: str = Form(...),
    tipo_prueba: str = Form(...),
    archivo: UploadFile = File(...)
):
    ext = os.path.splitext(archivo.filename)[1]
    if ext not in [".p", ".pickle"]:
        raise HTTPException(400, "Extensión no permitida")  # :contentReference[oaicite:4]{index=4}
    file_path = os.path.join(UPLOAD_DIR, archivo.filename)
    # guardado asíncrono con aiofiles :contentReference[oaicite:5]{index=5}
    async with aiofiles.open(file_path, "wb") as out:
        content = await archivo.read()
        await out.write(content)
    m = ModeloPrediccionCreate(
        nombre=nombre, descripcion=descripcion,
        version=version, tipo_prueba=tipo_prueba,
        archivo=file_path
    )
    return await create_modelo(m)

@router.get("/", response_model=list[ModeloPrediccionOut])
async def listar_modelos(skip: int = 0, limit: int = 100):
    return await get_modelos(skip, limit)
