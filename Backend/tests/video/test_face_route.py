import numpy as np
from src.database.crud import create_family_member, create_face_embedding
from src.database.schemas import FamilyMemberCreate, FaceEmbeddingCreate
from PIL import Image
import io


def create_test_image():
    img = Image.fromarray(np.ones((224, 224, 3), dtype=np.uint8) * 255)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def test_analyze_face_new_member(client, test_patient, mock_deepface):
    response = client.post(
        f"/face/analyze?patient_id={test_patient.id}",
        files={"file": ("test.png", create_test_image(), "image/png")},
    )
    print(response.json())

    assert response.status_code == 200


def test_analyze_face_existing_member(client, session, test_patient, mock_deepface):
    member = create_family_member(
        session,
        FamilyMemberCreate(
            patient_id=test_patient.id,
            name="John Doe",
            relation=None,
            phone=None,
        ),
    )

    create_face_embedding(
        session,
        FaceEmbeddingCreate(
            family_member=member.id,
            embedding=[0.1] * 128,
        ),
    )

    session.commit()

    response = client.post(
        f"/face/analyze?patient_id={test_patient.id}",
        files={"file": ("test.png", create_test_image(), "image/png")},
    )
    print(response.json())

    assert response.status_code == 200
