from app.crud.formularios import FormController
from app.schemas.modelos import ModeloPrediccionCreate
from app.schemas.modelos import ModeloPrediccionCreate
from app.database import modelos_collection
from bson import ObjectId
import os, shutil
from fastapi import HTTPException, status

from app.services.modelRegistry import load_model

UPLOAD_DIR = "uploads"

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


async def create_modelo(data: ModeloPrediccionCreate) -> dict:
    # 1) Verificar duplicado en BD
    exists = await modelos_collection.find_one({
        "nombre": data.nombre, "version": data.version
    })
    if exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe modelo '{data.nombre}' versión '{data.version}'"
        )                                            # 409 Conflict :contentReference[oaicite:2]{index=2}

    # 2) Preparar destino
    dest = os.path.join(UPLOAD_DIR, os.path.basename(data.archivo))
    
    # # 3) Evitar overwrite si ya existe
    # if os.path.exists(dest):
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail="Ya existe un archivo LOCAL con ese nombre en el servidor"
    #     )                                          # Evitar overwrite :contentReference[oaicite:3]{index=3}

    # 4) Mover el joblib temporal al destino final
    shutil.move(data.archivo, dest)               # mueve fichero :contentReference[oaicite:4]{index=4}
    data.archivo = dest

    # 5) Insertar en BD
    result = await modelos_collection.insert_one(data.dict())
    return modelo_helper({**data.dict(), "_id": result.inserted_id})


async def get_modelos(skip: int = 0, limit: int = 100) -> list[dict]:
    out = []
    cursor = modelos_collection.find().skip(skip).limit(limit)
    async for m in cursor:
        out.append(modelo_helper(m))
    return out

async def get_modelo_by_id(modelo_id: str) -> dict | None:
    m = await modelos_collection.find_one({"_id": ObjectId(modelo_id)})
    return modelo_helper(m) if m else None

async def get_modelos_by_name(nombre: str) -> list[dict]:
    out = []
    cursor = modelos_collection.find({"nombre": nombre})
    async for m in cursor:
        out.append(modelo_helper(m))
    return out  # :contentReference[oaicite:1]{index=1}

async def list_model_names() -> list[str]:
    # Distinct devuelve valores únicos :contentReference[oaicite:2]{index=2}
    return await modelos_collection.distinct("nombre")

async def list_versions_per_name() -> dict:
    names = await list_model_names()
    result = {}
    for n in names:
        result[n] = await modelos_collection.distinct("version", {"nombre": n})
    return result

async def delete_modelo(modelo_id: str) -> bool:
    res = await modelos_collection.delete_one({"_id": ObjectId(modelo_id)})
    return res.deleted_count == 1  # :contentReference[oaicite:4]{index=4}


async def predict(form_id: str, answers: dict) -> float:
    form = await FormController.get_formulario(form_id)
    if not form:
        raise ValueError("Formulario no encontrado")
    # Mapear respuestas al vector X según orden de preguntas :contentReference[oaicite:3]{index=3}
    X = [answers[q["id"]] for q in form["questions"]]
    model_path = form["model_name"] + "_" + form["model_version"] + ".pkl"
    model = load_model(model_path)
    pred = model.predict([X])[0]
    return float(pred)