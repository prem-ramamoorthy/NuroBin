from typing import Generator
from sqlalchemy import text
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.orm.session import Session as engSession

from src.config.config_env import Config

USERNAME = Config.POSTGRES_USERNAME
PASSWORD = Config.POSTGRES_PASSWORD
HOST = Config.POSTGRES_HOST
DATABASE = Config.POSTGRES_DB
DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:5432/{DATABASE}"


engine = create_engine(DATABASE_URL, pool_recycle=3600, echo=True)


def get_session() -> Generator[engSession, None, None]:
    with Session(engine) as session:
        yield session


def create_db_table():
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    for val in get_session():
        print(type(val))
