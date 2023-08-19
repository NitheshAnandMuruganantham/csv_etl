from fastapi import APIRouter, UploadFile, File, Depends
from services.uploads import UploadsService
from sqlalchemy.orm import Session
from dependency.db import get_db
from dependency.current_user import get_current_user
from schema.auth import SystemUser
import traceback

router = APIRouter(prefix="/upload", tags=["uploads"])


@router.post("/")
def upload(file: UploadFile = File(...),  db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    try:
        return UploadsService(db, 'weight/photos', {
            "org_id": user.org_id
        }).fileUpload(file)
    except Exception as e:
        traceback.print_exc()