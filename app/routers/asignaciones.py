from fastapi import APIRouter, HTTPException, status
from app.schemas.asignaciones import AsignacionCreate, AsignacionOut, AsignacionUpdate
from app.crud import asignaciones as crud_asignaciones

router = APIRouter()

@router.post("", response_model=AsignacionOut)
async def create_asignacion_route(asignacion: AsignacionCreate):
    return await crud_asignaciones.create_asignacion(asignacion)

@router.get("", response_model=list[AsignacionOut])
async def read_asignaciones(skip: int = 0, limit: int = 100):
    return await crud_asignaciones.get_asignaciones(skip, limit)

@router.get("/{asignacion_id}", response_model=AsignacionOut)
async def get_asignacion(asignacion_id: str):
    asignacion = await crud_asignaciones.get_asignacion_by_id(asignacion_id)
    if not asignacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asignación no encontrada"
        )
    return asignacion

@router.get("/userid/{user_id}", response_model=list[AsignacionOut])
async def get_asignacion(user_id: str):
    asignaciones = await crud_asignaciones.get_asignacion_by_userid(user_id)
    return asignaciones if asignaciones else []

@router.put("/{asignacion_id}", response_model=AsignacionOut)
async def update_asignacion_route(asignacion_id: str, asignacion_update: AsignacionUpdate):
    asignacion = await crud_asignaciones.get_asignacion_by_id(asignacion_id)
    if not asignacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asignación no encontrada"
        )
    updated_asignacion = await crud_asignaciones.update_asignacion(asignacion_id, asignacion_update)
    return updated_asignacion

@router.delete("/{asignacion_id}", response_model=AsignacionOut)
async def delete_asignacion_route(asignacion_id: str):
    asignacion = await crud_asignaciones.get_asignacion_by_id(asignacion_id)
    if not asignacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asignación no encontrada"
        )
    deleted = await crud_asignaciones.delete_asignacion(asignacion_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar la asignación"
        )
    return deleted