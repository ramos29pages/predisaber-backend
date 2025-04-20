# --- app/crud/modelos.py --- 
from app.schemas.modelos import ModeloPrediccionCreate
from app.database import modelos_collection
from bson import ObjectId

def modelo_helper(m) -> dict:
    return {
        "id": str(m["_id"]),
        "nombre": m["nombre"],
        "descripcion": m.get("descripcion"),
        "version": m["version"],
        "tipo_prueba": m["tipo_prueba"],
        "archivo": m["archivo"],
    }

async def create_modelo(m: ModeloPrediccionCreate) -> dict:
    doc = m.dict()
    res = await modelos_collection.insert_one(doc)
    new = await modelos_collection.find_one({"_id": res.inserted_id})
    return modelo_helper(new)

async def get_modelos(skip: int = 0, limit: int = 100) -> list:
    out = []
    cursor = modelos_collection.find().skip(skip).limit(limit)
    async for m in cursor:
        out.append(modelo_helper(m))
    return out

async def get_modelo(modelo_id: str) -> dict:
    m = await modelos_collection.find_one({"_id": ObjectId(modelo_id)})
    return modelo_helper(m) if m else None
