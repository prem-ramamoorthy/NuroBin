import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlmodel import SQLModel, Session, create_engine
import numpy as np

from src.database.models import Patient, User, UserRole
from src.main import app, get_session
from src.config.config_env import Config
from src.video import face_identification

USERNAME = Config.POSTGRES_USERNAME
PASSWORD = Config.POSTGRES_PASSWORD
HOST = Config.POSTGRES_HOST
DATABASE = "test_db"
TEST_DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:5432/{DATABASE}"

engine = create_engine(
    TEST_DATABASE_URL,
)


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture
def session():
    connection = engine.connect()
    transaction = connection.begin()

    session = Session(bind=connection)

    app.dependency_overrides[get_session] = lambda: session

    yield session

    session.close()
    transaction.rollback()
    connection.close()

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(session):
    user = User(
        username="testuser",
        email="test@example.com",
        password="hashedpassword",
        role=UserRole.patient,
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def test_patient(session, test_user):
    patient = Patient(
        user_id=test_user.id,
        name="Test Patient",
        age=30,
        address="123 Test Street",
        medical_history=None,
        phone="9999999999",
    )
    session.add(patient)
    session.commit()
    session.refresh(patient)
    return patient


@pytest.fixture
def mock_deepface(monkeypatch):
    def fake_extract_faces(**kwargs):
        return [{"face": np.ones((224, 224, 3), dtype=np.uint8)}]

    def fake_represent(**kwargs):
        return [{"embedding": [0.1] * 128}]

    monkeypatch.setattr(
        face_identification.detection,
        "extract_faces",
        fake_extract_faces,
    )

    monkeypatch.setattr(
        face_identification.representation,
        "represent",
        fake_represent,
    )
