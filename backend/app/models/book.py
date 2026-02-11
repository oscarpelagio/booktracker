"""Models de dades per a la base de dades."""

from sqlmodel import UniqueConstraint, Field

from app.schemas import BookBase


class Book(BookBase, table=True):
    """Model de base de dades per als llibres."""
    __tablename__ = "books"
    __table_args__ = (UniqueConstraint("title", "author", name="unique_book"),)

    id: int = Field(primary_key=True)
