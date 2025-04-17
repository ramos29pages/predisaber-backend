from fastapi import APIRouter, UploadFile, File, HTTPException, status, Form
import os
from app import crud
from app.models import ModeloPrediccionOut
import shutil

router = APIRouter()

# Asegurarse de que exista el directorio para los archivos subidos
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/", response_model=ModeloPrediccionOut)
async def registrar_modelo(
    nombre: str = Form(...),
    descripcion: str = Form(None),
    version: str = Form(...),
    tipo_prueba: str = Form(...),
    archivo: UploadFile = File(...)
):
    # Validar extensión del archivo
    ext = os.path.splitext(archivo.filename)[1]
    if ext not in [".p", ".pickle"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Extensión de archivo no permitida")
    
    # Guardar archivo en el directorio uploads
    file_location = os.path.join(UPLOAD_DIR, archivo.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)
    
    # Crear el documento del modelo
    modelo_data = {
        "nombre": nombre,
        "descripcion": descripcion,
        "version": version,
        "tipo_prueba": tipo_prueba,
        "archivo": file_location
    }
    nuevo_modelo = await crud.create_modelo(modelo_data)
    return nuevo_modelo

@router.get("/", response_model=list[ModeloPrediccionOut])
async def listar_modelos(skip: int = 0, limit: int = 100):
    return await crud.get_modelos(skip, limit)
