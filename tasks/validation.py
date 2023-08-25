from loguru import logger
from database.db import get_db_script
from services.uploads import UploadsService
from utils.batch_utils import calculate_batch_count
from repository.validation import ValidationRepository
import jsonschema
import json
import pandas as pd
import time
from utils.celery import celery
from utils.redis import get_redis
from utils.mongo import get_mongo
import sys
from uuid import uuid4 as uuid
from celery import group


@celery.task
def process_batch(args):
    pid = args["pid"]
    batch = args["batch"]
    schema = args["schema"]
    logger.info("Processing batch")
    errors = []
    warnings = []
    for row in batch:
        try:
            jsonschema.validate(instance=row, schema=schema)
        except jsonschema.ValidationError as err:
            errors.append({
                "row": json.loads(json.dumps(row, skipkeys=True)),
                "error": err.message,
                "type": "schema-error",
                "error_type": "error"
            })
    print("Batch processed")
    mongo = get_mongo()
    mongo[f"validation:{pid}"].insert_one({
        "errors": errors,
        "warnings": warnings
    })


@celery.task
def start_validation_csv(id, schema, schema_id, org_id, user_id, pid):
    overall_start_time = time.time()
    db = get_db_script()
    redis = get_redis()
    mongo = get_mongo()
    try:
        logger.info("Starting background validation", "id", id,
                    "schema_id", schema_id, "org_id", org_id)
        logger.info("Pulling file")
        file_pull_start_time = time.time()
        file = UploadsService(db,  'weight/photos', {
            "org_id": org_id
        }).get_file(id)
        file_pull_end_time = time.time()
        logger.info("schema pulled")

        read_csv_start_time = time.time()
        logger.info("Reading file")
        logger.info("processing to dataframe")
        df = pd.read_csv(file, low_memory=False)
        df = df.to_dict('records')
        read_csv_end_time = time.time()
        logger.info(
            f"File read execution_time {read_csv_end_time - read_csv_start_time}")
        errors = []
        warnings = []
        data = {
            "errors": [],
            "warnings": []
        }
        total_rows = len(df)
        process_start_time = time.time()
        redis.set(f"validation_{id}_status", "processing")
        batch_size = calculate_batch_count(total_rows)
        logger.info("Starting validation")
        batch_results = group(process_batch.s(
            {"batch": df[i:i + batch_size], "schema": schema, "pid": pid}) for i in range(0, len(df), batch_size)).apply_async()
        while not batch_results.ready():
            time.sleep(1)
        for record in mongo[f"validation:{pid}"].find():
            errors += record["errors"]
            warnings += record["warnings"]

        process_end_time = time.time()
        logger.info("Validation completed", "execution_time",
                    process_end_time - process_start_time)
        data["errors"] = errors
        data["warnings"] = warnings
        overall_end_time = time.time()
        data["metrics"] = {
            "total_rows": total_rows,
            "batch_size": batch_size,
            "total_errors": len(errors),
            "total_warnings": len(warnings),
            "execution_time": process_end_time - process_start_time,
            "file_pull_time": file_pull_end_time - file_pull_start_time,
            "overall_execution_time": overall_end_time - overall_start_time,
            "local_pid": pid,
            "user_id": user_id,
        }
        data["schema"] = schema
        data["schema_id"] = schema_id
        data["org_id"] = org_id
        data["file_id"] = id
        data["user_id"] = user_id
        data["status"] = "completed"
        data["created_at"] = time.time()
        start_time = time.time()
        logger.info("Uploading validation data")
        data_id = UploadsService(db,  'weight/photos', {
            "org_id": org_id
        }).upload_json(data, f"validation/{pid}_{id}.json")
        logger.info("Validation data uploaded")
        ValidationRepository(db, {
            "org_id": org_id
        }).create({
            "file_id": id,
            "data_id": data_id,
            "schema_id": schema_id,
        })
        end_time = time.time()
        logger.info("Validation data saved", "execution_time",
                    end_time - start_time)
        logger.info("Validation completed", "execution_time",
                    end_time - overall_start_time)
        redis.set(f"validation_{id}_status", "completed")
    except Exception as err:
        redis.set(f"validation_{id}_status", "failed")
        logger.error(err)
    finally:
        db.close()
