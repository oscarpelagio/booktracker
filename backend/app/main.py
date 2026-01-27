from fastapi import FastAPI, Depends
# from sqlalchemy.orm import Session
# from . import models, database

# # 1. Crear tablas en BBDD al iniciar (Magia de SQLAlchemy)
# models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Book Tracker API")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "El sistema está online 🚀"}