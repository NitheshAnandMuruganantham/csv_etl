from sqlalchemy import Column
from database.db import Base
from sqlalchemy import ForeignKey, BigInteger, String
from model.organization import OrganizationModel
from model.uploads import UploadsModel
from model.schema import SchemaModel
import time


class ValidationModel(Base):
    __tablename__ = "validation_data"
    id = Column(BigInteger, primary_key=True,
                nullable=False, autoincrement=True)
    file_id = Column(BigInteger, ForeignKey(UploadsModel.id), nullable=False)
    data_id = Column(BigInteger, ForeignKey(UploadsModel.id), nullable=False)
    schema_id = Column(BigInteger, ForeignKey(SchemaModel.id), nullable=False)
    created_at = Column(BigInteger, nullable=False, default=int(time.time()))
    pid = Column(String, nullable=True)
    org_id = Column(BigInteger, ForeignKey(
        OrganizationModel.id), nullable=False)
