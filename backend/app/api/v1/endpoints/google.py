"""Endpoints de l'API per a Google Books."""

from fastapi import APIRouter, Query, Depends
from sqlmodel import Session

from app.core.db import get_session
from app.crud import BookRepository
from app.schemas import BookResponse
from app.services import BookService

router = APIRouter()


def get_book_service(db: Session = Depends(get_session)) -> BookService:
    """Obté el servei de llibres amb el repositori injectat."""
    repo = BookRepository(db)
    return BookService(repo)


@router.get("/search-by-title", response_model=list[BookResponse])
async def search_by_title(
    title: str = Query(..., description="Títol del llibre a cercar"),
    service: BookService = Depends(get_book_service),
) -> list[BookResponse]:
    """
    Cerca llibres per títol.
    """
    books = await service.search_and_process(title)
    return [BookResponse.model_validate(book) for book in books]
