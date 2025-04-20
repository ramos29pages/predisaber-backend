# --- app/crud/pruebas.py ---
from app.schemas.pruebas import PruebaCreate
from app.database import pruebas_collection
from bson import ObjectId
import datetime

def prueba_helper(p) -> dict:
    return {
        "id": str(p["_id"]),
        "nombre": p["nombre"],
        "datos": p["datos"],
        "fecha": p["fecha"],
        "usuario_id": p["usuario_id"],
        "modelo_id": p["modelo_id"],
    }

async def create_prueba(p: PruebaCreate) -> dict:
    doc = p.dict()
    doc["fecha"] = datetime.datetime.utcnow()
    res = await pruebas_collection.insert_one(doc)
    new = await pruebas_collection.find_one({"_id": res.inserted_id})
    return prueba_helper(new)

async def get_pruebas(skip: int = 0, limit: int = 100) -> list:
    out = []
    cursor = pruebas_collection.find().skip(skip).limit(limit)
    async for p in cursor:
        out.append(prueba_helper(p))
    return out