from sqlalchemy import Column, String, JSON
from database.db import Base
from sqlalchemy import ForeignKey, BigInteger
from model.organization import OrganizationModel
from model.uploads import UploadsModel
import time


class SchemaModel(Base):
    __tablename__ = "schema_data"
    id = Column(BigInteger, primary_key=True,
                nullable=False, autoincrement=True)
    data = Column(JSON, nullable=False)
    type = Column(String, nullable=False)
    created_at = Column(BigInteger, nullable=False, default=int(time.time()))
    org_id = Column(BigInteger, ForeignKey(
        OrganizationModel.id), nullable=False)
