"""Servei de lògica de negoci per als llibres."""

import logging
from fastapi import HTTPException

from app.clients import GoogleBooksClient, get_google_books_client
from app.crud import BookRepository
from app.models import Book

logger = logging.getLogger(__name__)


class BookService:
    """
    Servei per gestionar la lògica de negoci dels llibres.
    
    Aquest servei s'encarrega de:
    - Cercar llibres a Google Books API (fins a 10 resultats)
    - Persistir llibres a la base de dades
    - Gestionar duplicats per títol+autor normalitzats
    """

    def __init__(
        self, 
        db_repo: BookRepository, 
        google_client: GoogleBooksClient | None = None
    ):
        """
        Inicialitza el servei amb les dependències necessàries.
        
        Args:
            db_repo: Repositori per accedir a la base de dades
            google_client: Client de Google Books (opcional, usa singleton per defecte)
        """
        self.repo = db_repo
        self.google_client = google_client or get_google_books_client()

    async def search_and_process(self, query: str) -> list[Book]:
        """
        Cerca llibres i els processa (fins a 10 resultats).
        
        Args:
            query: Terme de cerca
            
        Returns:
            Llista de llibres trobats o guardats (màxim 10)
            
        Raises:
            HTTPException: Si no es troben llibres (404) o hi ha error de connexió (503)
        """
        try:
            results = await self.google_client.search_books(query)
        except Exception as e:
            logger.error(f"Error cercant a Google Books: {e}")
            raise HTTPException(
                status_code=503, 
                detail="Error connectant amb Google Books"
            )

        if not results:
            raise HTTPException(
                status_code=404, 
                detail="Llibres no trobats a Google"
            )

        # Guarda tots els llibres (fins a 10)
        saved_books = []
        for book_data in results:
            try:
                # Intenta crear el llibre (o obtenir l'existent)
                saved_book = self.repo.create(book_data)
                if saved_book:
                    saved_books.append(saved_book)
                    logger.info(f"Llibre processat: {saved_book.title}")
            except Exception as e:
                logger.error(f"Error processant llibre '{book_data.title}': {e}")
                # Continua amb el següent llibre
                continue

        if not saved_books:
            raise HTTPException(
                status_code=500,
                detail="Error processant els llibres a la base de dades"
            )

        return saved_books
