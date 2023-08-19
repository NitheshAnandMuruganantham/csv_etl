from fastapi import APIRouter, Body, Depends, Request
from sqlalchemy.orm import Session
from dependency.db import get_db
from services.auth import AuthService
import datetime

router = APIRouter(prefix="/auth", tags=["auth"])

ENTITY = 'auth'


@router.post('/login', summary="Create access and refresh tokens for user")
def login(payload: dict = Body(...), db: Session = Depends(get_db)):
    username = payload.get("username")
    password = payload.get("password")
    response = AuthService(db).login(username, password)
  
    return response


@router.post('/refresh', summary="Refresh the access token")
def refresh(request: Request, db: Session = Depends(get_db)):
    return AuthService(db).refresh_token(request.headers.get("authorization").split(" ")[1])
