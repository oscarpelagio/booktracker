"""Client per a la API de Google Books amb patró Singleton."""

from functools import lru_cache
from typing import Self

import httpx
from datetime import date

from core.config import settings
from schemas import BookBase as Book


class GoogleBooksClient:
    """Client per a la API de Google Books amb reuse de connexions HTTP."""
    
    BASE_URL = "https://www.googleapis.com/books/v1/volumes"
    _instance: Self | None = None
    _client: httpx.AsyncClient | None = None

    def __new__(cls) -> Self:
        """Implementa el patró Singleton per assegurar una sola instància."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicialitza el client amb la API key de configuració."""
        if not hasattr(self, '_initialized'):
            self.api_key = settings.google_api_key
            self._initialized = True

    @property
    def client(self) -> httpx.AsyncClient:
        """Retorna el client HTTP, creant-lo si és necessari."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=30.0,
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
            )
        return self._client

    async def close(self):
        """Tanca el client HTTP de manera segura."""
        if self._client is not None and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    async def search_books(self, query: str, max_results: int = 10) -> list[Book]:
        """
        Cerca llibres a Google Books API.
        """
        # Google Books API màxim = 10 resultats per petició
        params = {
            "q": query, 
            "maxResults": max(1, min(max_results, 10))
        }
        if self.api_key:
            params["key"] = self.api_key

        response = await self.client.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "items" not in data:
            return []

        return [self._parse_book(item) for item in data["items"]]

    def _parse_book(self, item: dict) -> Book:
        """
        Converteix el JSON de Google en el model net amb validació.
        
        Args:
            item: Diccionari amb les dades de Google Books
            
        Returns:
            Instància de Book validada
        """
        volume = item.get("volumeInfo", {})

        # Extracció d'ISBN amb prioritat
        isbn = self._extract_isbn(volume.get("industryIdentifiers", []))

        # Parseig de la data de publicació
        published_date = self._parse_date(volume.get("publishedDate"))

        # Normalització d'autors i categories
        authors = self._normalize_list(volume.get("authors", ["Desconegut"]))
        categories = self._normalize_list(volume.get("categories", []))

        return Book(
            title=self._safe_get_string(volume, "title", "Sense títol"),
            author=authors,
            isbn=isbn,
            publisher=self._safe_get_string(volume, "publisher"),
            publisher_date=published_date,
            description=self._safe_get_string(volume, "description"),
            page_count=volume.get("pageCount") or 0,
            print_type=self._safe_get_string(volume, "printType", "BOOK"),
            categories=categories,
            maturity_rating=self._safe_get_string(volume, "maturityRating"),
            language=self._safe_get_string(volume, "language", "und"),
            preview_link=self._safe_get_string(volume, "previewLink"),
            small_thumbnail=self._safe_get_nested(volume, ["imageLinks", "smallThumbnail"]),
            thumbnail=self._safe_get_nested(volume, ["imageLinks", "thumbnail"]),
        )

    def _extract_isbn(self, identifiers: list[dict]) -> str:
        """Extreu l'ISBN amb prioritat a ISBN_13."""
        isbn_13 = None
        isbn_10 = None
        
        for identifier in identifiers:
            if identifier.get("type") == "ISBN_13":
                isbn_13 = identifier.get("identifier")
            elif identifier.get("type") == "ISBN_10":
                isbn_10 = identifier.get("identifier")
        
        return isbn_13 or isbn_10 or "Sense ISBN"

    def _parse_date(self, date_str: str | None) -> date | None:
        """Parseja dates en diferents formats (YYYY, YYYY-MM, YYYY-MM-DD)."""
        if not date_str:
            return None
            
        try:
            if len(date_str) == 4:  # YYYY
                return date(int(date_str), 1, 1)
            elif len(date_str) == 7:  # YYYY-MM
                parts = date_str.split("-")
                return date(int(parts[0]), int(parts[1]), 1)
            else:  # YYYY-MM-DD
                return date.fromisoformat(date_str)
        except (ValueError, IndexError):
            return None

    def _normalize_list(self, data: list[str] | str | None) -> str:
        """Normalitza llistes o strings a un string separat per comes."""
        if not data:
            return ""
        if isinstance(data, list):
            return ", ".join(data)
        return str(data)

    def _safe_get_string(self, data: dict, key: str, default: str = "") -> str:
        """Obté un valor string de forma segura."""
        value = data.get(key)
        return str(value) if value is not None else default

    def _safe_get_nested(self, data: dict, keys: list[str]) -> str | None:
        """Obté un valor de diccionaris niats de forma segura."""
        current = data
        for key in keys:
            if not isinstance(current, dict):
                return None
            current = current.get(key)
            if current is None:
                return None
        return current


@lru_cache()
def get_google_books_client() -> GoogleBooksClient:
    """
    Factory function que retorna una instància cachejada del client.
    
    Returns:
        Instància singleton de GoogleBooksClient
    """
    return GoogleBooksClient()
