from fastapi import HTTPException, status
from bson import ObjectId
from io import BytesIO
import joblib
import pandas as pd

from app.schemas.prediccion import PrediccionDatosEntrada
from app.database import fs_bucket, modelos_collection

async def generate_prediction(file_id: str, datos: PrediccionDatosEntrada):
    # 1) Validar ObjectId y existencia
    if not ObjectId.is_valid(file_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El file_id proporcionado no es un ObjectId válido"
        )
    doc = await modelos_collection.find_one({"file_id": file_id})
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró ningún modelo con file_id={file_id}"
        )

    stream = None
    try:
        # 2) Abrir stream
        stream = await fs_bucket.open_download_stream(ObjectId(file_id))
        # 3) Leer todos los bytes
        content_bytes = await stream.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al descargar el modelo: {e}"
        )
    finally:
        # 4) Cerrar síncronamente si se abrió
        if stream is not None:
            stream.close()

    # 5) Cargar modelo desde bytes
    buffer = BytesIO(content_bytes)
    try:
        modelo = joblib.load(buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al deserializar el modelo: {e}"
        )

    # 6) Preparar DataFrame y alinear columnas
    df = pd.DataFrame([datos.dict()])
    try:
        cols_esperadas = list(modelo.feature_names_in_)
        df = df.reindex(columns=cols_esperadas, fill_value=0)
    except AttributeError:
        pass

    # 7) Realizar predicción
    try:
        y = modelo.predict(df)
        return {
            "prediccion": int(y[0]),
            "file_id_usado": file_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al realizar la predicción: {e}"
        )
