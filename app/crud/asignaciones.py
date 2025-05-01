from typing import Optional
from bson import ObjectId

from fastapi import HTTPException, status
from app.schemas.asignaciones import AsignacionOut, AsignacionCreate
from app.database import asignaciones_collection


async def create_asignacion(asignacion: AsignacionCreate) -> AsignacionOut:
    # Validar duplicados por user_id y form_id
    existing = await asignaciones_collection.find_one({
        "user_id": asignacion.user_id,
        "form_id": asignacion.form_id
    })
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una asignación con este user_id y form_id."
        )
    
    # Crear nuevo documento
    asignacion_dict = asignacion.dict()
    result = await asignaciones_collection.insert_one(asignacion_dict)
    created = await asignaciones_collection.find_one({"_id": result.inserted_id})
    return AsignacionOut(**created, id=str(created["_id"]))

async def get_asignaciones(skip: int = 0, limit: int = 100) -> list[AsignacionOut]:
    cursor = asignaciones_collection.find().skip(skip).limit(limit)
    asignaciones = await cursor.to_list(length=limit)
    return [AsignacionOut(**a, id=str(a["_id"])) for a in asignaciones]

async def get_asignacion_by_id(id: str) -> Optional[AsignacionOut]:
    asignacion = await asignaciones_collection.find_one({"_id": ObjectId(id)})
    if asignacion:
        return AsignacionOut(**asignacion, id=str(asignacion["_id"]))
    return None

async def delete_asignacion(id: str) -> Optional[AsignacionOut]:
    asignacion = await asignaciones_collection.find_one_and_delete({"_id": id})
    if asignacion:
        return AsignacionOut(**asignacion, id=str(asignacion["_id"]))
    return None