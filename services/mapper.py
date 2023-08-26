from sqlalchemy.orm import Session
from repository.schema import SchemaRepository
from pandas import DataFrame


class MapperService():
    def __init__(self, db: Session, session):
        self.db = db
        self.schemaRepo = SchemaRepository(db, session)
        self.session = session
        self.org_id = session["org_id"]

    def map(self, df: DataFrame, schema):
        mapping = schema["mapping"]
        for col in mapping:
            df[col["to"]] = df[col["from"]]
        return df
