from sqlalchemy import Column, String, JSON
from database.db import Base
from model.organization import OrganizationModel
from sqlalchemy import BigInteger, ForeignKey,  DateTime, func, Integer
from enum import Enum


class InviteStatus(Enum):
    ACCEPTED = 1
    SENT = 2
    UNACCEPTED = 3


class UserRole(Enum):
    OPERATOR = 0
    MANAGER = 1
    ADMIN = 2
    DIRECTOR = 3
    HR = 4
    COMPLIANCE = 5
    SUPPORT = 6


class UserModel(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True,
                nullable=False, autoincrement=True)
    role = Column(BigInteger, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    password = Column(String, nullable=False)
    profile_data = Column(JSON, nullable=True, default={})
    access_token_hash = Column(String, nullable=True)
    refresh_token_hash = Column(String, nullable=True)
    last_login_at = Column(BigInteger, nullable=True)
    invite_status = Column(Integer, nullable=True, default=0)
    invite_token = Column(String, nullable=True)
    invite_token_expiry = Column(BigInteger, nullable=True)
    forgot_password_token = Column(String, nullable=True)
    forgot_password_token_expiry = Column(BigInteger, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    org_id = Column(BigInteger, ForeignKey(
        OrganizationModel.id), nullable=True)
