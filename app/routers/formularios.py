from fastapi import APIRouter, Depends, HTTPException
from typing import List

# Asumiendo que FormCreate y FormOut están definidos en 'app.schemas.formularios'
from app.schemas.formularios import FormCreate, FormOut

# Asumiendo que FormController está definido en 'app.controllers.formularios'
from app.crud.formController import FormController

router = APIRouter()

@router.post("/", response_model=FormOut, status_code=201)
async def create_formulario(formulario: FormCreate):
    return await FormController.create_formulario(formulario)

@router.get("/{formulario_id}", response_model=FormOut)
async def get_formulario(formulario_id: str):
    formulario = await FormController.get_formulario(formulario_id)
    if not formulario:
        raise HTTPException(status_code=404, detail="Formulario no encontrado")
    return formulario

@router.get("/", response_model=List[FormOut])
async def get_formularios(skip: int = 0, limit: int = 100):
    return await FormController.get_formularios(skip=skip, limit=limit)

@router.put("/{formulario_id}", response_model=FormOut)
async def update_formulario(formulario_id: str, formulario: FormOut):
    updated_formulario = await FormController.update_formulario(formulario_id, formulario)
    if not updated_formulario:
        raise HTTPException(status_code=404, detail="Formulario no encontrado")
    return updated_formulario

@router.delete("/{formulario_id}", response_model=FormOut)
async def delete_formulario(formulario_id: str):
    deleted_formulario = await FormController.delete_formulario(formulario_id)
    if not deleted_formulario:
        raise HTTPException(status_code=404, detail="Formulario no encontrado")
    return deleted_formulario