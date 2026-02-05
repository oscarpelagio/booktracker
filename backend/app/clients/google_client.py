import os
import httpx
from datetime import date
from app.models.book import Book


class GoogleBooksClient:
    BASE_URL = "https://www.googleapis.com/books/v1/volumes"

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")

    async def search_books(self, query: str, max_results: int = 5) -> list[Book]:
        params = {"q": query, "maxResults": max_results}
        if self.api_key:
            params["key"] = self.api_key

        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if "items" not in data:
                return []

            return [self._parse_book(item) for item in data["items"]]

    def _parse_book(self, item: dict) -> Book:
        """
        Método PRIVADO (Adapter): Convierte el JSON sucio de Google en tu Modelo limpio.
        """
        volume = item.get("volumeInfo", {})

        # 1. Extracción inteligente de ISBN (Prioridad ISBN_13 > ISBN_10)
        isbn = "Sin ISBN"
        identifiers = volume.get("industryIdentifiers", [])
        for i in identifiers:
            if i.get("type") == "ISBN_13":
                isbn = i.get("identifier")
                break
            elif i.get("type") == "ISBN_10":
                isbn = i.get("identifier")  # Fallback

        # 2. Limpieza de Fechas (Google es inconsistente aquí)
        pub_date_str = volume.get("publishedDate")
        published_date = None
        if pub_date_str:
            try:
                # Intentamos formatos comunes: YYYY-MM-DD, YYYY-MM, o YYYY
                if len(pub_date_str) == 4:  # Año solo "2021"
                    published_date = date(int(pub_date_str), 1, 1)
                elif len(pub_date_str) == 7:  # Año-Mes "2021-02"
                    parts = pub_date_str.split("-")
                    published_date = date(int(parts[0]), int(parts[1]), 1)
                else:  # Completa "2021-02-10"
                    published_date = date.fromisoformat(pub_date_str)
            except ValueError:
                pass  # Si falla (ej: "1858*"), dejamos None

        # 3. Limpieza de Autores y Categorías (Listas -> Strings)
        authors_list = volume.get("authors", ["Desconocido"])
        authors_str = (
            ", ".join(authors_list)
            if isinstance(authors_list, list)
            else str(authors_list)
        )

        categories_list = volume.get("categories", [])
        categories_str = (
            ", ".join(categories_list)
            if isinstance(categories_list, list)
            else str(categories_list)
        )

        # 4. Construcción del Objeto (Usando los nombres de tu modelo)
        # NOTA: Ajusta los nombres de la izquierda si cambiaste tu modelo a snake_case
        return Book(
            title=volume.get("title"),
            author=authors_str,
            isbn=isbn,
            publisher=volume.get("publisher"),
            publisher_date=published_date,
            description=volume.get("description"),
            page_count=volume.get("pageCount", 0),
            print_type=volume.get("printType"),
            categories=categories_str,
            maturity_rating=volume.get("maturityRating"),
            language=volume.get("language"),
            preview_link=volume.get("previewLink"),
            # Acceso seguro a diccionarios anidados para imágenes
            small_thumbnail=volume.get("imageLinks", {}).get("smallThumbnail"),
            thumbnail=volume.get("imageLinks", {}).get("thumbnail"),
        )
