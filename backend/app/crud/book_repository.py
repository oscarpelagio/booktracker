from sqlmodel import Session
from app.models.book import Book


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, book_data: Book) -> Book:
        book = Book.model_validate(book_data)
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book
