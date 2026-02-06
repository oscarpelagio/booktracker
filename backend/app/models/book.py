"""Models de dades per a la base de dades."""

from typing import Optional
from sqlmodel import Field, UniqueConstraint

from app.schemas import BookBase


class Book(BookBase, table=True):
    """Model de base de dades per als llibres."""
    __tablename__ = "books"
    __table_args__ = (UniqueConstraint("title", "author", name="unique_book"),)

    id: Optional[int] = Field(default=None, primary_key=True)
