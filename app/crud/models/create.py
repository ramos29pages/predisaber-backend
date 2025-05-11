import os
import aiofiles
from fastapi import HTTPException, status
from app.schemas.modelos import ModeloPrediccionCreate
from app.database import modelos_collection, fs_bucket

# Umbral en bytes (lo puedes ajustar si quieres tener un límite de tamaño)
# Aunque con GridFS, el límite principal es el de MongoDB.
MAX_FILE_SIZE = 200 * 1024 * 1024  # Ejemplo: 200 MB
UPLOAD_DIR = "uploads"

async def create_model(data: ModeloPrediccionCreate) -> dict:
    # 1) Verificar duplicado
    exists = await modelos_collection.find_one({
        "nombre": data.nombre, "version": data.version
    })
    if exists:
        os.remove(data.archivo)  # Limpiar el archivo temporal
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe modelo '{data.nombre}' versión '{data.version}'"
        )

    # 2) Verificar el tamaño del archivo (opcional, pero recomendado)
    file_path = data.archivo
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        os.remove(file_path)  # Limpiar el archivo temporal
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"El archivo excede el tamaño máximo permitido de {MAX_FILE_SIZE / (1024 * 1024)} MB."
        )

    doc = data.model_dump()
    doc.pop("archivo", None)  # Eliminamos la ruta temporal, solo guardamos file_id

    # 3) Almacenar el archivo usando GridFS
    try:
        # Abrimos y leemos todo el archivo
        async with aiofiles.open(file_path, "rb") as f:
            content = await f.read()

        # Subimos los bytes leídos
        file_id = await fs_bucket.upload_from_stream(
            os.path.basename(file_path), content
        )
        doc["file_id"] = str(file_id)
        os.remove(file_path)
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar el archivo en GridFS: {e}"
        )

    # 4) Insertar el documento y devolver resultado
    result = await modelos_collection.insert_one(doc)
    nuevo = await modelos_collection.find_one({"_id": result.inserted_id})
    return modelo_helper(nuevo)

def modelo_helper(m) -> dict:
    return {
        "id": str(m["_id"]),
        "nombre": m["nombre"],
        "descripcion": m.get("descripcion"),
        "version": m["version"],
        "creado_por": m["creado_por"],
        "precision": m["precision"],
        "date": m["date"],
        "variables": m["variables"],
        "file_id": m.get("file_id"),
    }