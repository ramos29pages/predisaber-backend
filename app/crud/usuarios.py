from app.database import usuarios_collection
from app.crud.asignaciones import delete_asignacion_by_userid
from app.schemas.usuarios import UsuarioCreate, UsuarioBase, UsuarioOut, UsuarioUpdate
from bson import ObjectId

def usuario_helper(usuario) -> dict:
    return {
        "id": str(usuario["_id"]),
        "name": usuario.get("name"),
        "email": usuario["email"],
        "role": usuario.get("role"),
        "semester": str(usuario.get("semester")),
        "identificacion": usuario.get("identificacion"),
        "tipo_prueba": usuario.get("tipo_prueba"),
        "picture": usuario.get("picture"),
    }

# CRUD para Usuarios
async def get_usuario_by_email(email: str):
    usuario = await usuarios_collection.find_one({"email": email})
    if usuario:
        return usuario_helper(usuario)
    return None


async def get_usuario_by_id(usuario_id: str) -> dict:
        usuario = await usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
        if usuario:
            return usuario_helper(usuario)
        return None

async def create_usuario(usuario: UsuarioCreate) -> dict:
    usuario_dict = {
        "name": usuario.name,
        "email": usuario.email,
        "role": usuario.role,
        "semester": str(usuario.semester),
        "identificacion": usuario.identificacion,
        "tipo_prueba": usuario.tipo_prueba,
        "picture": usuario.picture,
    }
    result = await usuarios_collection.insert_one(usuario_dict)
    new_usuario = await usuarios_collection.find_one({"_id": result.inserted_id})
    return usuario_helper(new_usuario)

async def get_usuarios(skip: int = 0, limit: int = 100) -> list:
    usuarios = []
    cursor = usuarios_collection.find().skip(skip).limit(limit)
    async for usuario in cursor:
        usuarios.append(usuario_helper(usuario))
    return usuarios

async def update_usuario(usuario_id: str, usuario_data: UsuarioBase) -> dict:
    # Cambio: usuario_data.dict() debe contener la clave 'nombre' en lugar de 'name'
    await usuarios_collection.update_one(
        {"_id": ObjectId(usuario_id)},
        {"$set": usuario_data.dict()}
    )
    usuario = await usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
    return usuario_helper(usuario)

async def delete_usuario(usuario_id: str) -> UsuarioOut | None:
    # 1) Borro la asignación asociada (si existe)
    await delete_asignacion_by_userid(usuario_id)
    
    # 2) Busco el usuario para devolver sus datos
    usuario = await usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
    if not usuario:
        return None
    
    # 3) Lo convierto a schema antes de borrarlo
    usuario_out = UsuarioOut(**usuario, id=str(usuario["_id"]))
    
    # 4) Borro el usuario
    await usuarios_collection.delete_one({"_id": ObjectId(usuario_id)})
    
    return usuario_out



async def update_usuario_picture(usuario_id: str, usuario_data: UsuarioUpdate) -> dict:
    # Sólo toma los campos enviados y no nulos
    update_dict = usuario_data.dict(exclude_unset=True, exclude_none=True)
    if not update_dict:
        return await get_usuario_by_id(usuario_id)

    await usuarios_collection.update_one(
        {"_id": ObjectId(usuario_id)},
        {"$set": update_dict}
    )
    usuario = await usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
    return usuario_helper(usuario)