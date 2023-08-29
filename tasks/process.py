from loguru import logger
from database.db import get_db_script
from services.uploads import UploadsService
from services.cleanup import CleanUpService
from services.mapper import MapperService
from services.transformer import TransformerService
from repository.output import OutputRepository
import pandas as pd
from utils.celery import celery
from utils.redis import get_redis
from utils.mongo import get_mongo
from .validation import start_validation_csv
import time


@celery.task
def process(id, schema, schema_id, org_id, user_id, pid, session):
    mongo = get_mongo()
    redis = get_redis()
    db = get_db_script()
    # validation_process = start_validation_csv.delay(
    #     id, schema, schema_id, org_id, user_id, pid)

    # while validation_process.status != "SUCCESS":
    #     time.sleep(1)

    logger.info(
        f"Starting background validation id {id} schema_id {schema_id} org_id {org_id}")
    logger.info("Pulling file")
    file_pull_start_time = time.time()
    file = UploadsService(db,  'weight/photos', {
        "org_id": org_id
    }).get_file(id)
    file_pull_end_time = time.time()
    logger.info(
        f"file pull execution_time {file_pull_end_time - file_pull_start_time}")
    read_csv_start_time = time.time()
    logger.info("Reading file")
    logger.info("processing to dataframe")
    df = pd.read_csv(file, low_memory=False)
    logger.info("processed dataframe")
    logger.info(f"df shape {df.shape}")
    logger.info("===========df==========")
    logger.info(df[:10])
    logger.info("===========df==========")

    read_csv_end_time = time.time()
    logger.info(
        f"File read execution_time {read_csv_end_time - read_csv_start_time}")
    logger.info("Starting cleanup")
    cleanup_start_time = time.time()
    df = CleanUpService(db, session).cleanup(df, schema)
    cleanup_end_time = time.time()
    logger.info(
        f"Cleanup completed execution_time {cleanup_end_time - cleanup_start_time}")
    logger
    logger.info("Starting mapping")
    mapping_start_time = time.time()
    df = MapperService(
        db, session).map(df, schema)
    mapping_end_time = time.time()
    logger.info(
        f"Mapping completed execution_time {mapping_end_time - mapping_start_time}")
    logger.info(f"df shape {df.shape}")
    logger.info("Starting transformation")
    transformation_start_time = time.time()
    transform = TransformerService(
        db, session)
    file_buffer = transform.transform(df, schema)
    file_name = transform.get_file_name(schema["transform"])
    transformation_end_time = time.time()
    logger.info(
        f"Transformation completed execution_time {transformation_end_time - transformation_start_time}")
    file_buffer.seek(0)
    logger.info("Starting upload")

    upload = UploadsService(db, 'weight/photos',
                            session).upload_fileobj(file_buffer.getvalue(), file_name)
    logger.info("Upload completed")
    OutputRepository(db, session).create({
        "file_id": id,
        "pid": pid,
        "data_id": upload,
        "schema_id": schema_id,
    })
    logger.info("Output created")
    redis.set(f"validation_{id}_status", "completed")
    mongo[f"validation:{pid}"].drop()
    return "ok"
