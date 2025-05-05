from fastapi import HTTPException, status
from typing import List, Optional
from bson import ObjectId
from app.schemas.resultados import ResultadoOut, ResultadoCreate
from app.database import resultados_collection

async def create_resultado(r: ResultadoCreate) -> ResultadoOut:
    """
    Inserta un documento en MongoDB; Mongo genera el _id.
    Convertimos ObjectId a str y lo asignamos a 'id'.
    """
    doc = r.model_dump()               # sólo los campos de entrada, sin id
    result = await resultados_collection.insert_one(doc)
    created = await resultados_collection.find_one({"_id": result.inserted_id})
    # convertimos a string y pasamos al modelo
    created["id"] = str(created["_id"])  
    return ResultadoOut(**created)

async def get_all_resultados(skip: int = 0, limit: int = 100) -> List[ResultadoOut]:
    cursor = resultados_collection.find().skip(skip).limit(limit)
    docs = await cursor.to_list(length=limit)
    # cada doc ya contiene ObjectId, pero Pydantic sólo espera str en 'id'
    return [ResultadoOut(**{**d, "id": str(d["_id"])}) for d in docs]

async def get_resultado_by_id(r_id: str) -> Optional[ResultadoOut]:
    doc = await resultados_collection.find_one({"_id": ObjectId(r_id)})
    if doc:
        doc["id"] = str(doc["_id"])
        return ResultadoOut(**doc)
    return None

async def delete_resultado(r_id: str) -> ResultadoOut:
    doc = await resultados_collection.find_one_and_delete({"_id": ObjectId(r_id)})
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resultado no encontrado")
    doc["id"] = str(doc["_id"])
    return ResultadoOut(**doc)
