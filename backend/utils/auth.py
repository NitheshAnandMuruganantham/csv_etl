from passlib.context import CryptContext
from settings import settings
import string
import secrets
from datetime import datetime, timedelta
from jose import jwt

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60 * 1000  # 30 days
REFRESH_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60 * 1000  # 30 days


def generatePassword():
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation
    alphabet = letters + digits + special_chars
    pwd = ''
    for i in range(5):
        pwd += ''.join(secrets.choice(alphabet))
    return pwd


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def decode_token(token: str) -> str:
    token = token.replace("Bearer ", "")
    return jwt.decode(token, settings.AUTH_SECRET, settings.AUTH_ALGORITHM)


def decode_refresh_token(token: str) -> str:
    token = token.replace("Bearer ", "")
    return jwt.decode(token, settings.AUTH_SECRET, settings.AUTH_ALGORITHM)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(data: dict) -> str:

    expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": "access_token"}
    to_encode.update(data)
    encoded_jwt = jwt.encode(
        to_encode, settings.AUTH_SECRET, settings.AUTH_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:

    expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": "refresh_token"}
    to_encode.update(data)
    encoded_jwt = jwt.encode(
        to_encode, settings.AUTH_SECRET, settings.AUTH_ALGORITHM)
    return encoded_jwt
