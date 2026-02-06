"""Paquet de clients per a APIs externes."""

from .google_client import GoogleBooksClient, get_google_books_client

__all__ = ["GoogleBooksClient", "get_google_books_client"]
