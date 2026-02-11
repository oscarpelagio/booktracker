"""Servei de lògica de negoci per als llibres."""

import logging
from fastapi import HTTPException

from clients import GoogleBooksClient, get_google_books_client
from crud import BookRepository
from models import Book

logger = logging.getLogger(__name__)


class BookService:

    def __init__(
        self, 
        db_repo: BookRepository, 
        google_client: GoogleBooksClient
    ):

        self.repo = db_repo
        self.google_client = google_client

    async def search_and_process(self, query: str) -> list[Book]:

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
