from sqlalchemy.orm import Session
from repository.schema import SchemaRepository
from pandas import DataFrame
from loguru import logger
import time


class CleanUpService():
    def __init__(self, db: Session, session):
        self.db = db
        self.schemaRepo = SchemaRepository(db, session)
        self.session = session
        self.org_id = session["org_id"]

    def cleanup(self, df: DataFrame, schema):
        logger.info("starting cleanup")
        start_time = time.time()
        schema = schema["clean_up"]
        emoji_treatment = schema["emoji_treatment"]
        nan_treatment = schema["nan_treatment"]

        if nan_treatment['action'] == 'drop':
            df.dropna(inplace=True)

        elif nan_treatment['action'] == 'replace':
            for col in nan_treatment['values']:
                df[col['column']].fillna(nan_treatment['value'], inplace=True)

        if emoji_treatment['action'] == 'drop':
            # df.astype(str).apply(lambda x: x.str.encode(
            #     'ascii', 'ignore').str.decode('ascii'))
            pass
        logger.info("===========cleanup==========")
        logger.info(df[:10])
        logger.info("===========cleanup==========")
        logger.info("cleanup completed")
        end_time = time.time()
        logger.info(
            f"Cleanup completed execution_time {end_time - start_time}")
        return df
