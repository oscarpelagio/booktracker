from fastapi import HTTPException
from app.clients.google_client import GoogleBooksClient
from app.crud.book_repository import BookRepository
from app.models.book import Book


class BookService:
    def __init__(self, db_repo: BookRepository):
        self.repo = db_repo
        self.google_client = GoogleBooksClient()

    async def search_and_process(self, query: str) -> Book:
        # 1. El cliente ya nos da una lista de OBJETOS Book (BookBase realmente)
        results = await self.google_client.search_books(query)

        if not results:
            raise HTTPException(status_code=404, detail="Libro no encontrado en Google")
        
        # 2. Nos quedamos con el primero
        candidate = results[0]

        # 3. Guardamos si tiene ISBN
        if candidate.isbn and candidate.isbn != "Sin ISBN":
            
            print(f"Guardando: {candidate.title}")
            return self.repo.create(candidate)
        
        return candidate