from fastapi import APIRouter, UploadFile, File, Depends
from services.validate import ValidationService
from sqlalchemy.orm import Session
from dependency.db import get_db
from dependency.current_user import get_current_user
from schema.auth import SystemUser


router = APIRouter(prefix="/validate", tags=["validation"])


@router.post("/")
def upload(id: str, schema: str, db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    return ValidationService(db, {
        "org_id": user.org_id,
        "user_id": user.id
    }).validate(id, schema)


@router.get("/")
def get_validation_data(id: str, db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    return ValidationService(db, {
        "org_id": user.org_id
    }).get_validation_data(id)
