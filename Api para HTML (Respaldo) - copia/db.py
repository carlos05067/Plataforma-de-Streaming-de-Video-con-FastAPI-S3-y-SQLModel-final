from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy import inspect

sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url)

def create_all_table(app:FastAPI):
    SQLModel.metadata.create_all(engine)
    if "categoria" not in {column["name"] for column in inspect(engine).get_columns("videos")}:
        with engine.begin() as connection:
            connection.exec_driver_sql(
                "ALTER TABLE videos ADD COLUMN categoria VARCHAR NOT NULL DEFAULT 'General'"
            )
    yield

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]