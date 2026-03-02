from pathlib import Path
from typing import Union
import numpy as np
from PIL import Image
from sqlmodel import Session
from deepface.modules import detection, representation
from deepface.modules.exceptions import SpoofDetected
from numpy.typing import NDArray
from typing import Any, Tuple, List, Dict, IO, cast
from src.database.crud import (
    create_face_embedding,
    create_family_member,
    get_closest_family_member,
)
from src.database.schemas import (
    FaceEmbeddingCreate,
    FamilyMemberCreate,
)

STORE_EMBEDDINGS = Path("./../memory/known_faces/")


def extract_faces_and_embeddings(
    img_path: Union[str, NDArray[Any], IO[bytes]],
    model_name: str = "VGG-Face",
    detector_backend: str = "opencv",
    enforce_detection: bool = True,
    align: bool = True,
    expand_percentage: int = 0,
    normalization: str = "base",
    anti_spoofing: bool = False,
) -> Tuple[List[List[float]], List[NDArray]]:
    """
    Extract facial areas and find corresponding embeddings for given image
    Returns:
        embeddings (List[float])
        facial areas (List[dict])
    """
    embeddings = []
    faces = []

    img_objs: List[Dict[str, Any]] = cast(
        List[Dict[str, Any]],
        detection.extract_faces(
            img_path=img_path,
            detector_backend=detector_backend,
            grayscale=False,
            enforce_detection=enforce_detection,
            align=align,
            expand_percentage=expand_percentage,
            anti_spoofing=anti_spoofing,
        ),
    )

    # find embeddings for each face
    for img_obj in img_objs:
        if anti_spoofing is True and img_obj.get("is_real", True) is False:
            raise SpoofDetected("Spoof detected in given image.")
        img_embedding_obj = representation.represent(
            img_path=img_obj["face"][
                :, :, ::-1
            ],  # make compatible with direct representation call
            model_name=model_name,
            enforce_detection=enforce_detection,
            detector_backend="skip",
            align=align,
            normalization=normalization,
        )
        # already extracted face given, safe to access its 1st item
        img_embedding_obj = cast(List[Dict[str, Any]], img_embedding_obj)
        img_embedding = img_embedding_obj[0]["embedding"]
        embeddings.append(img_embedding)
        faces.append(img_obj["face"])

    return (embeddings, faces)


def analyze_frame(
    session: Session, img: Union[Path, np.typing.NDArray, str], patientid: int
) -> Tuple[List[str], int]:
    if isinstance(img, Path):
        img = str(img)
    identities: List[str] = []
    count = 0
    embeddings, faces = extract_faces_and_embeddings(img_path=img)
    for embedding, face in zip(embeddings, faces):
        embedding_obj = cast(List[float], embedding)
        face_obj = cast(NDArray, face)
        member = get_closest_family_member(
            session, cast(List[float], embedding_obj), patientid
        )
        if member is None:
            new_relative = create_family_member(
                session,
                FamilyMemberCreate(
                    patient_id=patientid, name=None, relation=None, phone=None
                ),
            )
            create_face_embedding(
                session,
                FaceEmbeddingCreate(
                    family_member=new_relative.id, embedding=embedding_obj
                ),
            )
            id_dir = (
                STORE_EMBEDDINGS / str(new_relative.patient_id) / str(new_relative.id)
            )
            id_dir.mkdir(parents=True, exist_ok=True)
            image_path = id_dir / "face.png"
            Image.fromarray(face_obj).save(image_path)
            identities.append(f"Unknown individual {count}")
            count += 1
        else:
            if not member.name:
                identities.append(f"Unknown individual {count}")
                count += 1
            else:
                identities.append(member.name)
    return identities, count
