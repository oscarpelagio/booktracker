"""Repositori per a operacions CRUD de llibres."""

import unicodedata
import re
from sqlmodel import Session, select, func

from app.models import Book


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, book_data: Book) -> Book:
        """
        Crea un llibre nou. Si ja existeix (títol+autor normalitzats), retorna l'existent.
        
        Args:
            book_data: Dades del llibre a crear
            
        Returns:
            Llibre creat o l'existent si ja hi és
        """
        # Comprova si el llibre ja existeix per títol+autor normalitzats
        existing_book = self.find_by_title_author(
            book_data.title, 
            book_data.author
        )
        if existing_book:
            return existing_book
        
        book = Book.model_validate(book_data)
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def find_by_title_author(self, title: str, author: str) -> Book | None:
        """
        Cerca un llibre per títol i autor amb normalització.
        
        Compara els títols i autors normalitzats (minúscules, sense accents, etc.)
        però els guarda originals a la base de dades.
        
        Args:
            title: Títol del llibre
            author: Autor del llibre
            
        Returns:
            Llibre trobat o None si no existeix
        """
        # Normalitza el títol i autor per comparar
        normalized_title = self._normalize_text(title)
        normalized_author = self._normalize_text(author)
        
        # Busca tots els llibres i compara normalitzat
        # Nota: En una app gran, fariem la normalització a la BD amb un índex
        # Però per ara fem la comparació en Python
        statement = select(Book)
        result = self.db.exec(statement)
        books = result.all()
        
        for book in books:
            if (self._normalize_text(book.title) == normalized_title and 
                self._normalize_text(book.author) == normalized_author):
                return book
        
        return None

    def _normalize_text(self, text: str) -> str:
        """
        Normalitza text per comparació de duplicats.
        
        Transformacions:
        - Minúscules
        - Elimina accents (á → a, é → e, etc.)
        - Elimina espais extra
        - Elimina puntuació (!?.,; etc.)
        
        Args:
            text: Text a normalitzar
            
        Returns:
            Text normalitzat per comparació
        """
        if not text:
            return ""
        
        # Minúscules
        text = text.lower()
        
        # Elimina accents (NFD + filtra caràcters no ASCII + NFC)
        text = unicodedata.normalize('NFD', text)
        text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
        text = unicodedata.normalize('NFC', text)
        
        # Elimina puntuació: ! ? ¿ ¡ . , ; : ( ) [ ] { } " ' 
        text = re.sub(r'[!?¿¡.,;:\(\)\[\]{}"\']+', '', text)
        
        # Elimina espais al principi i final, i espais múltiples
        text = ' '.join(text.split())
        
        return text.strip()

    def get_by_id(self, book_id: int) -> Book | None:
        """Cerca un llibre pel seu ID."""
        return self.db.get(Book, book_id)

    def get_all(self) -> list[Book]:
        """Obté tots els llibres."""
        statement = select(Book)
        result = self.db.exec(statement)
        return result.all()

    def get_by_isbn(self, isbn: str) -> Book | None:
        """Cerca un llibre pel seu ISBN."""
        statement = select(Book).where(Book.isbn == isbn)
        result = self.db.exec(statement)
        return result.first()
