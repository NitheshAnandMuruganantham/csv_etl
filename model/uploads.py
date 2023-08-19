from sqlalchemy import Column, String
from database.db import Base
from sqlalchemy import ForeignKey, BigInteger
from model.organization import OrganizationModel


class UploadsModel(Base):
    __tablename__ = "uploads"
    id = Column(BigInteger, primary_key=True,
                nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    bucket = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    org_id = Column(BigInteger, ForeignKey(
        OrganizationModel.id), nullable=True)
