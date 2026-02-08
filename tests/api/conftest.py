import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

from src.main import app, get_session  # adjust import if needed


TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)


def override_get_session():
    with Session(engine) as session:
        yield session


@pytest.fixture
def session():
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture()
def client():
    return TestClient(app)
