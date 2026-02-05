from fastapi import APIRouter, Query, Depends
from sqlmodel import Session
from app.core.db import get_session
from app.services.book_service import BookService
from app.crud.book_repository import BookRepository
from app.models.book import Book

router = APIRouter()


# Función auxiliar para inyectar el servicio
def get_book_service(db: Session = Depends(get_session)) -> BookService:
    repo = BookRepository(db)
    return BookService(repo)


@router.get("/search-by-title", response_model=Book)
async def search_by_title(
    title: str = Query(...), service: BookService = Depends(get_book_service)
):
    """
    Busca por título. El servicio se encarga de buscar en Google
    y guardar en local si es necesario.
    """
    return await service.search_and_process(title)
