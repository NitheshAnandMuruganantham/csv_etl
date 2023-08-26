
from fastapi import HTTPException
from sqlalchemy.orm import Session
from loguru import logger
from repository.schema import SchemaRepository
from services.uploads import UploadsService
from repository.validation import ValidationRepository
from repository.output import OutputRepository
import traceback
from uuid import uuid4 as uuid
from tasks.process import process
from utils.redis import get_redis


class ValidationService:
    def __init__(self, db: Session, session):
        self.db = db
        self.validationRepo = ValidationRepository(db, session)
        self.schemaRepo = SchemaRepository(db, session)
        self.session = session
        self.org_id = session["org_id"]

    def validate(self, id, schema_id):
        logger.info("Validating", "id", id, "schema_id", schema_id)
        logger.info("pulling schema")

        try:
            schema = self.schemaRepo.findOne(schema_id).data
        except:
            traceback.print_exc()
            logger.error("Schema not found", "id", id, "schema_id", schema_id)
            raise HTTPException(
                status_code=404, detail="Schema not found")
        pid = uuid()
        process.delay(
            id,
            schema,
            schema_id,
            self.org_id,
            self.session["user_id"],
            pid,
            self.session
        )
        get_redis().set(
            f"validation_status_{self.session['user_id']}_{pid}", "started")
        return {
            "id": pid,
            "message": "Validation started"
        }

    def get_validation_data(self, upload_id, pid=None):
        data = []
        filters = {
            "file_id__eq": upload_id,
        }
        if pid is not None:
            filters["pid__eq"] = pid
        resp = self.validationRepo.findAll(filters)

        upload_service = UploadsService(self.db,  'weight/photos', {
            "org_id": self.org_id
        })

        for row in resp:
            row = row.__dict__
            row["url"] = upload_service.download(row["data_id"])
            data.append(row)
        return data

    def get_output_file(self, upload_id, pid=None):
        data = []
        filters = {
            "file_id__eq": upload_id,
        }
        if pid is not None:
            filters["pid__eq"] = pid
        resp = OutputRepository(self.db, self.session).findAll(filters)

        upload_service = UploadsService(self.db,  'weight/photos', {
            "org_id": self.org_id
        })

        for row in resp:
            row = row.__dict__
            row["url"] = upload_service.download(row["data_id"])
            data.append(row)
        return data
