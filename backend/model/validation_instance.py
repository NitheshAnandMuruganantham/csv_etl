from sqlalchemy import Column, Integer,  BigInteger, JSON, UUID
from database.db import Base
from model.schema import SchemaModel
from model.organization import OrganizationModel
from model.uploads import UploadsModel
from sqlalchemy import ForeignKey


class ValidationInstanceModel(Base):
    __tablename__ = 'validation_instance'

    id = Column(UUID, primary_key=True)
    created_At = Column(BigInteger, nullable=True)
    picked_at = Column(BigInteger, nullable=True)
    validation_start_time = Column(BigInteger, nullable=True)
    validation_end_time = Column(BigInteger, nullable=True)
    transformed_start_time = Column(BigInteger, nullable=True)
    transform_end_time = Column(BigInteger, nullable=True)
    map_start_time = Column(BigInteger, nullable=True)
    map_end_time = Column(BigInteger, nullable=True)
    csv_read_time = Column(BigInteger, nullable=True)
    csv_size = Column(Integer, nullable=True)
    csv_row_len = Column(Integer, nullable=True)
    upload_start = Column(BigInteger, nullable=True)
    upload_end = Column(BigInteger, nullable=True)
    pull_start = Column(BigInteger, nullable=True)
    pull_end = Column(BigInteger, nullable=True)
    status = Column(Integer, default=0)
    output_status = Column(Integer, default=0)
    mapping_status = Column(Integer, default=0)
    cleanup_status = Column(Integer, default=0)
    validation_status = Column(Integer, default=0)
    transform_status = Column(Integer, default=0)
    map_status = Column(Integer, default=0)
    end_time = Column(BigInteger, nullable=True)
    enqueue_time = Column(BigInteger, nullable=True)
    schema_pull_time = Column(BigInteger, nullable=True)
    upload_id = Column(Integer, ForeignKey(UploadsModel.id))
    schema_id = Column(Integer, ForeignKey(SchemaModel.id))
    schema = Column(JSON)
    progress_percentage = Column(Integer, default=0)
    org_id = Column(Integer, ForeignKey(OrganizationModel.id))
    transformation_end_time = Column(BigInteger, nullable=True)
    cleanup_start_time = Column(BigInteger, nullable=True)
    read_csv_start_time = Column(BigInteger, nullable=True)
    mapping_end_time = Column(BigInteger, nullable=True)
    read_csv_end_time = Column(BigInteger, nullable=True)
    mapping_start_time = Column(BigInteger, nullable=True)
    file_pull_end_time = Column(BigInteger, nullable=True)
    transformation_start_time = Column(BigInteger, nullable=True)
    cleanup_end_time = Column(BigInteger, nullable=True)
    file_pull_start_time = Column(BigInteger, nullable=True)
    created_at = Column(BigInteger, nullable=True)
