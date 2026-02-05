import os
from sqlmodel import SQLModel, create_engine, Session

# Credenciales del .env
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST", "db")
port = os.getenv("POSTGRES_PORT", "5432")
db_name = os.getenv("POSTGRES_DB")

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
