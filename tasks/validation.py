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
from celery import group


@celery.task
def process_batch(args):
    redis = get_redis()
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
                "key": err.absolute_path[0],
                "type": "schema-error",
                "error_type": "error"
            })
    print("Batch processed")
    mongo = get_mongo()
    if len(errors) > 0:
        redis.set(f"validation_{pid}_status", "failed")
    mongo[f"validation:{pid}"].insert_one({
        "errors": errors,
        "warnings": warnings
    })


@celery.task
def start_validation_csv(id, schema, schema_id, org_id, user_id, pid):
    schema = schema["validation"]
    overall_start_time = time.time()
    db = get_db_script()
    redis = get_redis()
    mongo = get_mongo()
    try:
        logger.info(
            f"Starting background validation id {id} schema_id {schema_id} org_id {org_id}")
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
        df = pd.read_csv(file, engine='pyarrow', low_memory=False)
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
        logger.info(f"Batch size {batch_size}")
        logger.info("Starting validation")
        batch = []
        for i in range(0, len(df), batch_size):
            batch.append({
                "batch": df[i:i + batch_size],
                "schema": schema,
                "pid": pid
            })
        batch_results = group(process_batch.s(i) for i in batch).apply_async()
        while not batch_results.ready():
            time.sleep(1)
        for record in mongo[f"validation:{pid}"].find():
            errors += record["errors"]
            warnings += record["warnings"]

        process_end_time = time.time()
        logger.info(
            f"Validation completed execution_time {process_end_time - process_start_time}")
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
        logger.info(data)
        data_id = UploadsService(db,  'weight/photos', {
            "org_id": org_id
        }).upload_json(data, f"validation/{pid}_{id}.json")
        logger.info("Validation data uploaded")
        ValidationRepository(db, {
            "org_id": org_id
        }).create({
            "file_id": id,
            "pid": pid,
            "data_id": data_id,
            "schema_id": schema_id,
        })
        end_time = time.time()
        logger.info(
            f"Validation data saved execution_time {end_time - start_time}")
        logger.info(
            f"Validation completed execution_time: {end_time - overall_start_time}")
        redis.set(f"validation_{id}_status", "completed")
    except Exception as err:
        redis.set(f"validation_{id}_status", "failed")
        logger.error(err)
    finally:
        db.close()
