from loguru import logger
from database.db import get_db_script
from services.uploads import UploadsService
from utils.batch_utils import calculate_batch_size
from repository.validation import ValidationRepository
import jsonschema
import json
import pandas as pd
import time
from utils.celery import celery
from celery import group
from utils.redis import get_redis
from utils.mongo import get_mongo


@celery.task
def process_batch(args):
    pid = args["pid"]
    logger.info("Processing batch")
    print("=====================================")
    print(args["batch"][:3])
    print("=====================================")
    errors = []
    warnings = []
    for row in args["batch"]:
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
    mongo = get_mongo()
    mongo[f"validation:{pid}"].insert_one({
        "errors": errors,
        "warnings": warnings
    })


@celery.task
def validate(args):
    pid = args["pid"]
    df = args["df"]
    schema = args["schema"]

    batch_size = calculate_batch_size(len(df))

    batch_results = group(process_batch.s(
        {"batch": df[i:i + batch_size], "schema": schema, "pid": pid}) for i in range(0, len(df), batch_size)).apply_async()
    return batch_results


@celery.task
def start_validation_csv(id, schema, schema_id, org_id, user_id, pid):
    db = get_db_script()
    redis = get_redis()
    mongo = get_mongo()
    try:
        logger.info("Starting background validation", "id", id,
                    "schema_id", schema_id, "org_id", org_id)
        logger.info("Pulling file")
        file = UploadsService(db,  'weight/photos', {
            "org_id": org_id
        }).get_file(id)
        logger.info("File pulled")
        logger.info("Reading file")
        start_time = time.time()
        df = []
        logger.info("Reading file")
        df = pd.read_csv(file)
        df.fillna(0, inplace=True)
        df = df.to_dict('records')
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info("File read", "execution_time", execution_time)
        logger.info("File read")

        logger.info("Batch processing completed")
        data = {
            "errors": [],
            "warnings": []
        }
        batch_processing_task = validate.delay({
            "pid": pid,
            "df": df,
            "schema": schema
        })
        logger.info("Waiting for validation sub-processes to complete")

        while not batch_processing_task.ready():
            pass
        logger.info("Validation completed")
        logger.info("Uploading validation data")
        batch_results = mongo[f"validation:{pid}"].find()
        for result in batch_results:
            data["errors"].extend(result["errors"])
            data["warnings"].extend(result["warnings"])
        logger.info("Validation completed", "id", id,
                    "schema_id", schema_id, "org_id", org_id)
        logger.info("Uploading validation data")
        data_id = UploadsService(db,  'weight/photos', {
            "org_id": org_id
        }).upload_json(data, f"validation/{id}.json")
        logger.info("Validation data uploaded")
        ValidationRepository(db, {
            "org_id": org_id
        }).create({
            "file_id": id,
            "data_id": data_id,
            "schema_id": schema_id,
        })
        redis.set(
            f"validation_status_{user_id}_{pid}", "completed")
        # mongo[f"validation:{pid}"].drop()
        # mongo[f"validation:{pid}"].delete_many({})
        db.close()
    except Exception as err:
        logger.error(err)
        redis.set(
            f"validation_status_{user_id}_{pid}", "error")
        mongo[f"validation:{pid}"].drop()
        db.close()
        raise err
