from fastapi import APIRouter, Body, Depends
from services.schema import SchemaService
from sqlalchemy.orm import Session
from dependency.db import get_db
from schema.auth import SystemUser
from dependency.current_user import get_current_user
from utils.repo import rowToDict
router = APIRouter(prefix="/schema", tags=["schema"])

ENTITY = 'customers'


@router.post("/")
def post(id: int = None, body: dict = Body(...), db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    session = {
        'id': user.id,
        'org_id': user.org_id,
        'role': user.role,
        'email': user.email
    }
    service = SchemaService(db, session)
    if (id is not None):
        response = service.update(id, body)
        response = service.findOne(id)
    else:
        response = service.create(body)

    return response


@router.post("/get")
def get(id: int = None, filters: dict = None, skip: int = None, take: int = None, group_by: str = None, db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    service = SchemaService(db, {
        'id': user.id,
        'org_id': user.org_id,
        'role': user.role,
        'email': user.email
    })
    if (id is not None):
        return service.findOne(id)

    return service.findAll(filters, group_by, take, skip)


@router.delete("/")
def delete(id: int, db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    session = {
        'id': user.id,
        'org_id': user.org_id,
        'role': user.role,
        'email': user.email
    }
    data = SchemaService(db, session).findOne(id)
    deleted = SchemaService(db, session).delete(id)
    return deleted


@router.post("/count")
def search(filters: dict = None, db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    return SchemaService(db, {
        'id': user.id,
        'org_id': user.org_id,
        'role': user.role,
        'email': user.email
    }).count(filters)
