from fastapi import APIRouter
from app.api.v1.endpoints import google  # Importamos el archivo de endpoints

api_router = APIRouter()

# Registro de rutas
api_router.include_router(google.router, prefix="/google", tags=["Google Books API"])