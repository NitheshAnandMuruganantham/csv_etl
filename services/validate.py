
import pandas as pd
from fastapi import HTTPException
import numpy as np
from sqlalchemy.orm import Session
import jsonschema
from loguru import logger
import multiprocessing as mp
from services.s3 import S3Service
from model.validation import ValidationModel
from services.uploads import UploadsService
import json
from database.db import get_db_script
import math
from model.schema import SchemaModel
import csv
import time


def calculate_batch_size(num_rows, num_cores, target_memory_usage_per_core_mb=500):
    logger.info("Calculating batch size", "num_rows", num_rows)
    memory_per_core_bytes = target_memory_usage_per_core_mb * 1024 * 1024
    row_size_bytes = memory_per_core_bytes / num_cores

    batch_size = max(1, math.floor(row_size_bytes / num_rows))
    logger.info(f"total rows: {num_rows}")
    logger.info(f"total cores: {num_cores}")
    logger.info(f"memory per core: {memory_per_core_bytes}")
    logger.info(f"Batch size calculated: {batch_size}")
    return batch_size


def background_validation(id, schema, schema_id, org_id):
    logger.info("Starting background validation", "id", id,
                "schema_id", schema_id, "org_id", org_id)
    db = get_db_script()
    logger.info("Pulling file")
    file = UploadsService(db,  'weight/photos', {
        "org_id": org_id
    }).get_file(id)
    logger.info("File pulled")
    logger.info("Reading file")
    start_time = time.time()
    df = []
    logger.info("Reading file")
    for row in csv.DictReader(file):
        df.append(row)
    end_time = time.time()
    execution_time = end_time - start_time
    logger.info("File read", "execution_time", execution_time)
    logger.info("File read")
    num_processes = mp.cpu_count()
    batch_size = calculate_batch_size(len(df), num_processes)

    batches = [{"rows": df[i:i + batch_size], "schema": schema}
               for i in range(0, len(df), batch_size)]

    with mp.Pool(processes=num_processes) as pool:
        results = pool.map(process_batch, batches)
        data = {
            "errors": [],
            "warnings": []
        }
        for result in results:
            data["errors"].extend(result["errors"])
            data["warnings"].extend(result["warnings"])
        logger.info("Validation completed", "id", id,
                    "schema_id", schema_id, "org_id", org_id)
        logger.info("Uploading validation data")
        data_id = UploadsService(db,  'weight/photos', {
            "org_id": org_id
        }).upload_json(data, f"validation/{id}.json")
        logger.info("Validation data uploaded")
        db.add(ValidationModel(
            file_id=id,
            data_id=data_id,
            schema_id=schema_id
        ))
        db.commit()


def process_batch(args):
    logger.info("Processing batch")
    errors = []
    warnings = []
    for row in args["rows"]:
        try:
            jsonschema.validate(instance=row, schema=args["schema"])
        except jsonschema.ValidationError as err:
            errors.append({
                "row": json.loads(json.dumps(row, skipkeys=True)),
                "error": err.message,
                "type": "schema-error",
                "error_type": "error"
            })
    print("Batch processed")
    return {
        "errors": errors,
        "warnings": warnings
    }


class ValidationService:
    def __init__(self, db: Session, session):
        self.db = db
        self.session = session
        self.org_id = session["org_id"]

    def validate(self, id, schema_id):
        logger.info("Validating", "id", id, "schema_id", schema_id)
        logger.info("pulling schema")
        schema = self.db.query(SchemaModel.data).filter(
            SchemaModel.id == schema_id, SchemaModel.type == "validation").first()
        try:
            schema = schema[0]
        except:
            logger.error("Schema not found", "id", id, "schema_id", schema_id)
            raise HTTPException(
                status_code=404, detail="Schema not found")
        mp.Process(target=background_validation, args=(
            id, schema, schema_id, self.org_id)).start()
        return "Validation started"

    def get_validation_data(self, upload_id):
        data = []
        resp = self.db.query(ValidationModel).filter(
            ValidationModel.file_id == upload_id).all()
        upload_service = UploadsService(self.db,  'weight/photos', {
            "org_id": self.org_id
        })
        for row in resp:
            row = row.__dict__
            row["url"] = upload_service.download(row["data_id"])
            data.append(row)
        return data
