from app.schemas.usuarios import UsuarioCreate, UsuarioBase
from app.schemas.modelos import ModeloPrediccionCreate 
from app.schemas.pruebas import PruebaCreate
from app.database import usuarios_collection, modelos_collection, pruebas_collection
from passlib.context import CryptContext
import datetime
from bson import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funciones de ayuda para formatear documentos (convertir _id a string)
def usuario_helper(usuario) -> dict:
    return {
        "id": str(usuario["_id"]),
        # Cambio: se renombra 'name' a 'nombre' para coincidir con el modelo Pydantic
        "name": usuario.get("name"),
        "email": usuario["email"],
        "role": usuario.get("role"),
        "semester": str(usuario.get("semester")),
        "identificacion": usuario.get("identificacion"),
        "tipo_prueba": usuario.get("tipo_prueba"),
        "picture": usuario.get("picture"),
    }

def modelo_helper(modelo) -> dict:
    return {
        "id": str(modelo["_id"]),
        "nombre": modelo["nombre"],
        "descripcion": modelo.get("descripcion"),
        "version": modelo["version"],
        "tipo_prueba": modelo["tipo_prueba"],
        "archivo": modelo["archivo"],
    }

def prueba_helper(prueba) -> dict:
    return {
        "id": str(prueba["_id"]),
        "nombre": prueba["nombre"],
        "datos": prueba["datos"],
        "fecha": prueba["fecha"],
        "usuario_id": prueba["usuario_id"],
        "modelo_id": prueba["modelo_id"],
    }

# CRUD para Usuarios
# async def get_usuario_by_email(email: str):
#     usuario = await usuarios_collection.find_one({"email": email})
#     if usuario:
#         return usuario_helper(usuario)
#     return None

# async def create_usuario(usuario: UsuarioCreate) -> dict:
#     usuario_dict = {
#         "name": usuario.name,
#         "email": usuario.email,
#         "role": usuario.role,
#         "semester": str(usuario.semester),
#         "identificacion": usuario.identificacion,
#         "tipo_prueba": usuario.tipo_prueba,
#         "picture": usuario.picture,
#     }
#     result = await usuarios_collection.insert_one(usuario_dict)
#     new_usuario = await usuarios_collection.find_one({"_id": result.inserted_id})
#     return usuario_helper(new_usuario)

# async def get_usuarios(skip: int = 0, limit: int = 100) -> list:
#     usuarios = []
#     cursor = usuarios_collection.find().skip(skip).limit(limit)
#     async for usuario in cursor:
#         usuarios.append(usuario_helper(usuario))
#     return usuarios

# async def update_usuario(usuario_id: str, usuario_data: UsuarioBase) -> dict:
#     # Cambio: usuario_data.dict() debe contener la clave 'nombre' en lugar de 'name'
#     await usuarios_collection.update_one(
#         {"_id": ObjectId(usuario_id)},
#         {"$set": usuario_data.dict()}
#     )
#     usuario = await usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
#     return usuario_helper(usuario)

# async def delete_usuario(usuario_id: str) -> dict:
#     usuario = await usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
#     if usuario:
#         await usuarios_collection.delete_one({"_id": ObjectId(usuario_id)})
#         return usuario_helper(usuario)
#     return None

# CRUD para Modelos de Predicción
async def create_modelo(modelo_data: dict) -> dict:
    # Se espera que 'modelo_data' incluya los campos: nombre, descripcion, version, tipo_prueba, y archivo
    result = await modelos_collection.insert_one(modelo_data)
    nuevo_modelo = await modelos_collection.find_one({"_id": result.inserted_id})
    return modelo_helper(nuevo_modelo)

async def get_modelos(skip: int = 0, limit: int = 100) -> list:
    modelos = []
    cursor = modelos_collection.find().skip(skip).limit(limit)
    async for modelo in cursor:
        modelos.append(modelo_helper(modelo))
    return modelos

async def get_modelo(modelo_id: str) -> dict:
    modelo = await modelos_collection.find_one({"_id": ObjectId(modelo_id)})
    if modelo:
        return modelo_helper(modelo)
    return None

# CRUD para Pruebas
async def create_prueba(prueba: PruebaCreate) -> dict:
    prueba_dict = prueba.dict()
    prueba_dict["fecha"] = datetime.datetime.utcnow()
    result = await pruebas_collection.insert_one(prueba_dict)
    nueva_prueba = await pruebas_collection.find_one({"_id": result.inserted_id})
    return prueba_helper(nueva_prueba)

async def get_pruebas(skip: int = 0, limit: int = 100) -> list:
    pruebas = []
    cursor = pruebas_collection.find().skip(skip).limit(limit)
    async for prueba in cursor:
        pruebas.append(prueba_helper(prueba))
    return pruebas