from fastapi import FastAPI
import uvicorn
from app.routers import users, modelos, pruebas, formularios, asignaciones, resultados
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API de Gestión de Modelos y Pruebas con MongoDB Atlas")

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Gestión de Modelos y Pruebas con MongoDB"}

app.include_router(users.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(modelos.router, prefix="/modelos", tags=["Modelos de Predicción"])
app.include_router(pruebas.router, prefix="/pruebas", tags=["Pruebas"])
app.include_router(formularios.router, prefix="/formularios", tags=["Formularios"])
app.include_router(asignaciones.router, prefix="/asignaciones", tags=["Asignaciones"])
app.include_router(resultados.router, prefix="/resultados", tags=["Resultados"])

if __name__ == "__main__":
    uvicorn.run("app.main:app.main", host="0.0.0.0", port=8000, reload=True, log_level="info")
