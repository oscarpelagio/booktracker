"""Esquemes de validació per a l'API."""

from datetime import date
from typing import Optional
from sqlmodel import SQLModel


class BookBase(SQLModel):
    """Esquema base amb camps comuns."""
    title: str
    author: str
    publisher: Optional[str] = None
    publisher_date: Optional[date] = None
    description: Optional[str] = None
    isbn: str
    page_count: Optional[int] = None
    print_type: Optional[str] = None
    categories: Optional[str] = None
    maturity_rating: Optional[str] = None
    small_thumbnail: Optional[str] = None
    thumbnail: Optional[str] = None
    language: str
    preview_link: Optional[str] = None


class BookCreate(BookBase):
    """Esquema per crear un llibre nou."""
    pass


class BookUpdate(SQLModel):
    """Esquema per actualitzar un llibre existent."""
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    publisher_date: Optional[date] = None
    description: Optional[str] = None
    isbn: Optional[str] = None
    page_count: Optional[int] = None
    print_type: Optional[str] = None
    categories: Optional[str] = None
    maturity_rating: Optional[str] = None
    small_thumbnail: Optional[str] = None
    thumbnail: Optional[str] = None
    language: Optional[str] = None
    preview_link: Optional[str] = None


class BookResponse(BookBase):
    """Esquema de resposta de l'API."""
    id: int

    class Config:
        from_attributes = True


class BookSearchResponse(SQLModel):
    """Esquema per respostes de cerca."""
    query: str
    total_results: int
    books: list[BookResponse]
