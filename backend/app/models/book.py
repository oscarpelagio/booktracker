from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field, UniqueConstraint


class BookBase(SQLModel):
    __tablename__ = "books"
    __table_args__ = UniqueConstraint("title", "author", name="unique_book")

    id: str | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    publisher: str
    publisher_date: date
    description: str
    isbn: str
    page_count: int
    print_type: str
    categories: str
    maturity_rating: str
    small_thumbnail: str
    thumbnail: str
    language: str
    preview_link: str


class Book(BookBase, table=True):
    __tablename__ = "books"
    __table_args__ = (UniqueConstraint("title", "author", name="unique_book"),)

    id: Optional[int] = Field(default=None, primary_key=True)
