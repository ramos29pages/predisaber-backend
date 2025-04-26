from app.database import usuarios_collection, modelos_collection, pruebas_collection, formularios_collection

def get_db():
    return {
        "usuarios": usuarios_collection,
        "modelos": modelos_collection,
        "pruebas": pruebas_collection,
        "formularios": formularios_collection
    }
