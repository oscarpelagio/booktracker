from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.v1.router import api_router

# En un futuro estas migraciones se harán con Alembic
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Book Tracker API")

app.include_router(api_router)

# Raiz del back
@app.get("/", tags=["Backend"])
def status(): 
    return {"status": "ok", "message": "Running"}