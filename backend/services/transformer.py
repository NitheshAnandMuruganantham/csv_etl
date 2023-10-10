from sqlalchemy.orm import Session
from repository.schema import SchemaRepository
from pandas import DataFrame
from io import StringIO
from uuid import uuid4 as uuid
from loguru import logger
import time


class TransformerService():
    def __init__(self, db: Session, session):
        self.db = db
        self.schemaRepo = SchemaRepository(db, session)
        self.session = session
        self.org_id = session["org_id"]

    def transform(self, df: DataFrame, schema):
        logger.info("starting transform")
        start_time = time.time()
        transform = schema["transform"]
        logger.info("===========pre-transform==========")
        logger.info(df[:10])
        logger.info("===========pre-transform==========")
        csv_buffer = StringIO()
        if transform == "xlsx":
            logger.info("transforming to xlsx")
            output = df.to_excel(csv_buffer, index=False)
        elif transform == "csv":
            logger.info("transforming to csv")
            output = df.to_csv(csv_buffer, index=False)
        elif transform == "json":
            logger.info("transforming to json")
            output = df.to_json(csv_buffer, index=False)
        elif transform == "html":
            logger.info("transforming to html")
            output = df.to_html(csv_buffer, index=False)
            logger.info("transform completed")
            end_time = time.time()
            logger.info(
                f"Transform completed execution_time {end_time - start_time}")

        return csv_buffer

    def get_file_name(self, file_type):
        if file_type == "xlsx":
            return f"{uuid()}.xlsx"
        elif file_type == "csv":
            return f"{uuid()}.csv"
        elif file_type == "json":
            return f"{uuid()}.json"
        elif file_type == "html":
            return f"{uuid()}.html"
