from fastapi import APIRouter, HTTPException, status
from typing import List
from app.crud.generations.generate import generate_prediction
from app.schemas.resultados import ResultadoOut, ResultadoCreate
from app.schemas.prediccion import PrediccionDatosEntrada, PrediccionOut
from app.crud import resultados as crud
import joblib
import pandas as pd
import numpy as np

router = APIRouter()

@router.post("", response_model=ResultadoOut, status_code=status.HTTP_201_CREATED)
async def create_resultado(r: ResultadoCreate):
    """
    Crea un nuevo Resultado. El id lo genera MongoDB.
    """
    return await crud.create_resultado(r)

@router.get("", response_model=List[ResultadoOut])
async def list_resultados(skip: int = 0, limit: int = 100):
    """
    Lista todos los Resultados con paginación.
    """
    return await crud.get_all_resultados(skip, limit)

@router.post("/predecir/{file_id}")
async def predecir(file_id: str, datos: PrediccionDatosEntrada):
    try:
        prediccion = await generate_prediction(file_id, datos)
    except FileNotFoundError:
        raise HTTPException(404, file_id)

    return prediccion
    

@router.get("/{resultado_id}", response_model=ResultadoOut)
async def get_resultado(resultado_id: str):
    """
    Obtiene un Resultado por su id.
    """
    res = await crud.get_resultado_by_id(resultado_id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resultado no encontrado"
        )
    return res

@router.delete("/{resultado_id}", response_model=ResultadoOut)
async def delete_resultado(resultado_id: str):
    """
    Elimina un Resultado por su id.
    """
    return await crud.delete_resultado(resultado_id)
