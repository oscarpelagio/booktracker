from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.db import create_db_and_tables
from app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Book Tracker API", lifespan=lifespan)

app.include_router(api_router)

@app.get("/", tags=["Backend"])
def status():
    return {"status": "ok", "message": "Running"}