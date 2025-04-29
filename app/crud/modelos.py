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
        "archivo": m["archivo"],
        "creado_por": m["creado_por"],
        "precision": m["precision"],
        "date": m["date"],
        "variables": m["variables"],
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

async def update_modelo(modelo_id: str, data: ModeloPrediccionCreate) -> dict:
    # 1) Validar ID válido
    if not ObjectId.is_valid(modelo_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "ID inválido")

    # 2) Buscar original
    orig = await modelos_collection.find_one({"_id": ObjectId(modelo_id)})
    if not orig:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Modelo no encontrado")


        # Evitar colisión al cambiar nombre/version
    if "nombre" in data or "version" in data:
        other = await modelos_collection.find_one({
            "nombre": data.get("nombre"),
            "version": data.get("version"),
            "_id": {"$ne": ObjectId(modelo_id)}
        })
        if other:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Otro modelo ya usa ese nombre y versión en la DB"
            )
            
    # 3) Si envían nuevo archivo, procesarlo
    new_file = data.get("archivo")
    if new_file:
        dest = os.path.join(UPLOAD_DIR, os.path.basename(new_file))
        # Verificar colisión
        # if os.path.exists(dest):
        #     raise HTTPException(
        #         status_code=status.HTTP_409_CONFLICT,
        #         detail="Ya existe un archivo con ese nombre en el servidor"
        #     )
        # Borrar antiguo
        if os.path.isfile(orig["archivo"]):
            os.remove(orig["archivo"])
        # Mover el nuevo
        shutil.move(new_file, dest)
        # Actualiza la ruta en el dict
        data["archivo"] = dest
    else:
        # conserva la ruta anterior si no se envió nuevo archivo
        data["archivo"] = orig["archivo"]

    # 4) Actualizar campos en BD
    await modelos_collection.update_one(
        {"_id": ObjectId(modelo_id)},
        {"$set": data}
    )                                              # update_one :contentReference[oaicite:7]{index=7}

    updated = await modelos_collection.find_one({"_id": ObjectId(modelo_id)})
    return modelo_helper(updated)


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