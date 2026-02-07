from sqlmodel import SQLModel, Session, create_engine
from src.database import models

USERNAME = "postgres"
PASSWORD = "mysecretpassword"
HOST = "localhost"
DATABASE = "nurobin"
DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:5432/{DATABASE}"


engine = create_engine(DATABASE_URL, pool_recycle=3600, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
