from fastapi import APIRouter, HTTPException, status
from app import controller
from app.schemas.pruebas import PruebaCreate, PruebaOut

router = APIRouter()

@router.post("/", response_model=PruebaOut)
async def registrar_prueba(prueba: PruebaCreate):
    # Se podría agregar validación adicional según el tipo de prueba y el modelo seleccionado.
    nueva_prueba = await controller.create_prueba(prueba)
    return nueva_prueba

@router.get("/", response_model=list[PruebaOut])
async def listar_pruebas(skip: int = 0, limit: int = 100):
    return await controller.get_pruebas(skip, limit)
