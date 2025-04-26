from app.schemas.modelos import ModeloPrediccionCreate
from app.database import modelos_collection
from app.services.modelRegistry import load_model
from app.crud.formularios import FormController
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

async def create_modelo(data: ModeloPrediccionCreate) -> dict:
    doc = data.dict()
    res = await modelos_collection.insert_one(doc)
    new = await modelos_collection.find_one({"_id": res.inserted_id})
    return modelo_helper(new)

async def get_modelos(skip: int = 0, limit: int = 100) -> list[dict]:
    out = []
    cursor = modelos_collection.find().skip(skip).limit(limit)
    async for m in cursor:
        out.append(modelo_helper(m))
    return out

async def get_modelo(modelo_id: str) -> dict | None:
    m = await modelos_collection.find_one({"_id": ObjectId(modelo_id)})
    return modelo_helper(m) if m else None

async def predict(form_id: str, answers: dict) -> float:
    form = await FormController.get_formulario(form_id)
    if not form:
        raise ValueError("Formulario no encontrado")
    # Mapear respuestas al vector X según orden de preguntas :contentReference[oaicite:3]{index=3}
    X = [answers[q["id"]] for q in form["questions"]]
    model_path = form["model_name"] + "_" + form["model_version"] + ".pkl"
    model = load_model(model_path)
    pred = model.predict([X])[0]
    return float(pred)