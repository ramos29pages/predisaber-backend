import aiofiles
import os
from bson import ObjectId
from app.database import modelos_collection, fs_bucket


async def update_model(modelo_id: str, update_data: dict) -> dict:
    # 1) Si hay campo "archivo", subimos a GridFS y reemplazamos por file_id
    if "archivo" in update_data:
        file_path = update_data.pop("archivo")
        # Leemos bytes y subimos
        async with aiofiles.open(file_path, "rb") as f:
            content = await f.read()
        file_id = await fs_bucket.upload_from_stream(
            os.path.basename(file_path), content
        )
        # Añadimos el nuevo file_id
        update_data["file_id"] = str(file_id)

        # (Opcional) Borrar el file anterior en GridFS:
        antiguo = await modelos_collection.find_one({"_id": ObjectId(modelo_id)})
        if antiguo and antiguo.get("file_id"):
            try:
                await fs_bucket.delete(ObjectId(antiguo["file_id"]))
            except Exception:
                pass  # ignoramos fallo al borrar antiguo

    # 2) Ejecutamos el update
    result = await modelos_collection.update_one(
        {"_id": ObjectId(modelo_id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise ValueError("No existe modelo con ese ID")
    # 3) Recuperamos el documento actualizado
    actualizado = await modelos_collection.find_one({"_id": ObjectId(modelo_id)})
    return modelo_helper(actualizado)

def modelo_helper(m) -> dict:
    return {
        "id": str(m["_id"]),
        "nombre": m["nombre"],
        "descripcion": m.get("descripcion"),
        "version": m["version"],
        "creado_por": m["creado_por"],
        "precision": m["precision"],
        "date": m["date"],
        "variables": m["variables"],
        "file_id": m.get("file_id"),
    }