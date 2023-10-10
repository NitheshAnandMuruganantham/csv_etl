from sqlalchemy import Column, String, JSON
from database.db import Base
from sqlalchemy import BigInteger, Boolean,  DateTime, func


class OrganizationModel(Base):
    __tablename__ = "organizations"
    id = Column(BigInteger, primary_key=True,
                nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True, unique=True)
    phone = Column(String, nullable=True, unique=True)
    company = Column(String, nullable=True)
    user_id = Column(String, nullable=True)
    address = Column(String, nullable=True)
    gstin = Column(String, nullable=True)
    profile_data = Column(JSON, nullable=True, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted = Column(Boolean, nullable=True, default=False)
