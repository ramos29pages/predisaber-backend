from typing import Optional
from bson import ObjectId
from datetime import datetime

from fastapi import HTTPException, status
from app.schemas.asignaciones import AsignacionOut, AsignacionCreate, AsignacionUpdate
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

async def update_asignacion(id: str, asignacion_update: AsignacionUpdate) -> Optional[AsignacionOut]:
    update_data = asignacion_update.dict(exclude_unset=True)
    if "status" in update_data and update_data["status"] is True and "completed_at" not in update_data:
        update_data["completed_at"] = datetime.utcnow().isoformat()

    result = await asignaciones_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": update_data},
        return_document=True
    )
    if result:
        return AsignacionOut(**result, id=str(result["_id"]))
    return None

async def delete_asignacion(id: str) -> Optional[AsignacionOut]:
    asignacion = await asignaciones_collection.find_one_and_delete({"_id": ObjectId(id)})
    if asignacion:
        return AsignacionOut(**asignacion, id=str(asignacion["_id"]))
    return None

async def get_asignacion_by_userid(user_id: str) -> Optional[AsignacionOut]:
    asignacion = await asignaciones_collection.find_one({"user_id": user_id})
    if asignacion:
        return AsignacionOut(**asignacion, id=str(asignacion["_id"]))
    return None