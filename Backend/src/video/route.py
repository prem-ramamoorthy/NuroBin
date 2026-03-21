from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlmodel import Session
from pathlib import Path
import shutil
import tempfile

from src.database.create_tables import get_session
from src.video.face_identification import analyze_frame

router = APIRouter(prefix="/face", tags=["Face"])


@router.post("/analyze")
def analyze_face(
    patient_id: int,
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    """
    Upload an image and analyze faces.
    """

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = Path(tmp.name)

        identities, count = analyze_frame(
            session=session,
            img=tmp_path,
            patientid=patient_id,
        )

        return {
            "identities": identities,
            "new_unknown_count": count,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
