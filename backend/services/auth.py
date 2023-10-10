from fastapi import status, HTTPException
from repository.users import UserRepository
from services.mail import MailService
from sqlalchemy.orm import Session
from utils.auth import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    verify_password
)
import traceback
import math
import random
from uuid import uuid4 as uuid
import datetime

FAKE_PASSWORD = "asokdA87fnf30efjoiOI**cwjkn"


class AuthService(UserRepository):

    def __init__(self, db: Session):
        self.db = db
        super().__init__(db)

    def generateOTP(len):

        digits = "0123456789"
        OTP = ""

        for i in range(len):
            OTP += digits[math.floor(random.random() * 10)]

        return OTP

    def login(self, email, password):

        try:
            print("email " + email)
            user = super().findByEmail(email)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect email or password"
                )

            hashed_pass = user['password']
            if not verify_password(password, hashed_pass):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect email or password"
                )

            user_dict = {
                "id": user['id'],
                "org_id": user['org_id'],
                "email": user['email'],
                "role": user['role']
            }

            response = {
                "access_token": create_access_token(user_dict),
                "refresh_token": create_refresh_token(user_dict),
            }

            [user.pop(key) for key in ['password', 'forgot_password_token',
                                       'refresh_token_hash', 'access_token_hash', 'invite_token']]

            response.update(user)

        except Exception:
            print(traceback.format_exc())
            raise (HTTPException(status_code=401, detail="Login Failed "))

        return response

    def resetPassword(self, email):
        token = self.generateOTP()
        expiry = datetime.datetime.now() + datetime.timedelta(days=5)
        super().updateByEmail(email, {
            "forgot_password_token": hash(token),
            "forgot_password_token_expiry": expiry.timestamp()
        })

        MailService().send_password_reset(email, token)
        return "ok"

    def changePassword(self, email, password, token):
        user = super().findByEmail(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password"
            )

        if (hash(token) == user['forgot_password_token']):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect token"
            )

        if datetime.datetime.now().timestamp() > user['forgot_password_token_expiry']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token expired"
            )

        super().updateByEmail(email, {
            "password": get_hashed_password(password),
            "forgot_password_token": None,
            "forgot_password_token_expiry": None
        })
        return "ok"

    def inviteUser(self, user):
        try:
            invite_token = str(uuid())
            hashed_invite_token = hash(invite_token)
            expiry = datetime.datetime.now() + datetime.timedelta(days=5)
            expiry_timestamp = expiry.timestamp()

            resp = super().create({
                "name": user["name"],
                "email": user["email"],
                "phone": user.get("phone", None),
                "address": user.get("address", None),
                "password": get_hashed_password("@!$SOME$RANDOMpass"),
                "role": user["role"],
                "invite_token": hashed_invite_token,
                "invite_status": 2,
                "invite_token_expiry": expiry_timestamp
            })
            try:
                MailService().send_invite(user["email"], invite_token)
            except:
                pass
            return resp
        except Exception as e:
            print(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error sending invite"
            )

    def acceptInvite(self, email, password, token):
        try:
            print("email " + email)

            user = super().findByEmail(email)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect email or password"
                )

            if (hash(token) == user['invite_token']):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect token"
                )

            if datetime.datetime.now().timestamp() > user['invite_token_expiry']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Token expired"
                )

            super().updateByEmail(email, {
                "password": get_hashed_password(password),
                "invite_token": None,
                "invite_status": 1,
                "invite_token_expiry": None
            })
            return "ok"
        except Exception as e:
            print(traceback.format_exc())

    def refresh_token(self, token):
        try:
            decoded = decode_refresh_token(token)
            user = super().findByEmail(decoded['email'])
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect email or password"
                )

            user_dict = {
                "id": user['id'],
                "org_id": user["org_id"],
                "email": user['email'],
                "role": user['role']
            }

            response = {
                "access_token": create_access_token(user_dict),
                "refresh_token": create_refresh_token(user_dict),
            }

            [user.pop(key) for key in ['password', 'forgot_password_token',
                                       'refresh_token_hash', 'access_token_hash', 'invite_token']]

            response.update(user)

        except Exception:
            print(traceback.format_exc())
            raise (HTTPException(status_code=401, detail="Refresh Token Failed "))

        return response
