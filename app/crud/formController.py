# Asumiendo que 'formularios_collection' está importado desde tu configuración de base de datos
from app.database import formularios_collection
from app.schemas.formularios import FormCreate, FormBase
from bson import ObjectId

# Función helper para formatear documentos de formulario
def formulario_helper(formulario) -> dict:
    return {
        "id": str(formulario["_id"]),
        "name": formulario["name"],
        "description": formulario.get("description"),
        "logo": formulario.get("logo"),
        "questions": formulario["questions"],
    }

class FormController:
    @staticmethod
    async def create_formulario(formulario: FormCreate) -> dict:
        formulario_dict = formulario.dict()
        result = await formularios_collection.insert_one(formulario_dict)
        nuevo_formulario = await formularios_collection.find_one({"_id": result.inserted_id})
        return formulario_helper(nuevo_formulario)

    @staticmethod
    async def get_formulario(formulario_id: str) -> dict:
        formulario = await formularios_collection.find_one({"_id": ObjectId(formulario_id)})
        if formulario:
            return formulario_helper(formulario)
        return None

    @staticmethod
    async def get_formularios(skip: int = 0, limit: int = 100) -> list:
        formularios = []
        cursor = formularios_collection.find().skip(skip).limit(limit)
        async for formulario in cursor:
            formularios.append(formulario_helper(formulario))
        return formularios

    @staticmethod
    async def update_formulario(formulario_id: str, formulario_data: FormBase) -> dict:
        await formularios_collection.update_one(
            {"_id": ObjectId(formulario_id)},
            {"$set": formulario_data.dict(exclude_unset=True)}
        )
        formulario = await formularios_collection.find_one({"_id": ObjectId(formulario_id)})
        if formulario:
            return formulario_helper(formulario)
        return None

    @staticmethod
    async def delete_formulario(formulario_id: str) -> dict:
        formulario = await formularios_collection.find_one({"_id": ObjectId(formulario_id)})
        if formulario:
            await formularios_collection.delete_one({"_id": ObjectId(formulario_id)})
            return formulario_helper(formulario)
        return None