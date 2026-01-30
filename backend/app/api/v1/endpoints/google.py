from fastapi import APIRouter, HTTPException, Query
import httpx

router = APIRouter(tags=["Google Books API"])

GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"

# Búsqueda de un libro por título y autor
@router.get("/search")
async def search(title: str = Query(...), author: str = Query(...)):
    async with httpx.AsyncClient() as client:
        q = f"intitle:{title}+inauthor:{author}"        
        resp = await client.get(GOOGLE_BOOKS_URL, params={"q": q, "maxResults": 1})
        data = resp.json()

    if "items" not in data:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    volume = data["items"][0]["volumeInfo"]
    return {
        "title": volume.get("title"),
        "author": ", ".join(volume.get("authors", ["Desconocido"])),
        "isbn": next((i["identifier"] for i in volume.get("industryIdentifiers", []) if i["type"] == "ISBN_13"), "Sin ISBN")
    }
