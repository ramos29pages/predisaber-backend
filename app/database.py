from motor.motor_asyncio import AsyncIOMotorClient
import os

# Se puede configurar la conexión con variables de entorno. Por ejemplo:
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb+srv://dramosm21:1tgv3EbaP9zxLlJ1@predisaber.nckhyp1.mongodb.net/?retryWrites=true&w=majority&appName=predisaber")

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client["predisaber"]

usuarios_collection = database.get_collection("usuarios")
modelos_collection = database.get_collection("modelos_prediccion")
pruebas_collection = database.get_collection("pruebas")
formularios_collection = database.get_collection("formularios")
asignaciones_collection = database.get_collection("asignaciones")
resultados_collection = database.get_collection("resultados")
