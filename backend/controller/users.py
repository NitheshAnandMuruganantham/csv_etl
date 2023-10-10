from fastapi import APIRouter, Body, Depends, HTTPException
from services.users import UserService
from sqlalchemy.orm import Session
from dependency.db import get_db
from schema.auth import SystemUser
from dependency.current_user import get_current_user
from utils.repo import rowToDict
router = APIRouter(prefix="/users", tags=["users"])

ENTITY = 'users'


@router.post("/")
def post(id: int = None, request: dict = Body(...), db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    session = {
        'id': user.id,
        "org_id": user.org_id,
        "role": user.role,
        "email": user.email,
    }
    userService = UserService(db, session)
    if (id is not None):
        response = userService.update(id, request)
        user = userService.findOne(id)
   
    else:
        response = userService.create(request)
    return response


@router.post("/get")
def get(id: int = None, filters: dict = None, group_by: str = None, take: int = None, skip: int = None, db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    userService = UserService(db, {
        'id': user.id,
        "org_id": user.org_id,
        "role": user.role,
        "email": user.email,
    })
    if (id is not None):
        return userService.findOne(id)
    return userService.findAll(filters, group_by, take, skip)


@router.post("/count")
def get(filters: dict = None, db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    return UserService(db, {'id': user.id,
                            "org_id": user.org_id,
                            "role": user.role,
                            "email": user.email, }).count(filters)


@router.delete("/")
def delete(id: int, db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    session = {
        'id': user.id,
        "org_id": user.org_id,
        "role": user.role,
        "email": user.email, }

    userService = UserService(db, session)

    user = userService.findOne(id)
    if (user is not None):
        raise HTTPException(status_code=400, detail="User not found")
    userService.delete(id)
 


@router.get("/search")
def delete(search: str = "", db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    return UserService(db, {
        "id": user.id,
        "org_id": user.org_id,
        "role": user.role,
        "email": user.email, }).search(search)


@router.get("/roles")
def get_roles(db: Session = Depends(get_db), user: SystemUser = Depends(get_current_user)):
    return UserService(db, {
        "id": user.id,
        "org_id": user.org_id,
        "role": user.role,
        "email": user.email, }).getRoles()
