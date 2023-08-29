from sqlalchemy.orm import Session
from repository.schema import SchemaRepository
from pandas import DataFrame
from loguru import logger
import time


class MapperService():
    def __init__(self, db: Session, session):
        self.db = db
        self.schemaRepo = SchemaRepository(db, session)
        self.session = session
        self.org_id = session["org_id"]

    def map(self, df: DataFrame, schema):
        start_time = time.time()
        logger.info("starting mapping")
        mapping = schema["mapping"]
        for col in mapping:
            df[col["to"]] = df[col["from"]]
        logger.info("===========mapping==========")
        logger.info(df[:10])
        logger.info("===========mapping==========")
        end_time = time.time()
        logger.info(
            f"Mapping completed execution_time {end_time - start_time}")

        return df
