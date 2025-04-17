from fastapi import FastAPI
from app.routers import users, modelos, pruebas

app = FastAPI(title="API de Gestión de Modelos y Pruebas con MongoDB Atlas")

app.include_router(users.router, prefix="/users", tags=["Usuarios"])
app.include_router(modelos.router, prefix="/modelos", tags=["Modelos de Predicción"])
app.include_router(pruebas.router, prefix="/pruebas", tags=["Pruebas"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
