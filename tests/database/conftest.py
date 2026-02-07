import pytest
from sqlmodel import SQLModel, Session, create_engine
from src.database.models import Patient, Doctor, CareTaker


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
