"""Rutes principals de l'API."""

from fastapi import APIRouter
from app.api.v1.endpoints import router as google_router

api_router = APIRouter()

api_router.include_router(google_router, prefix="/google", tags=["Google Books API"])
