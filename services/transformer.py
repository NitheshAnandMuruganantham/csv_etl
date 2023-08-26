from sqlalchemy.orm import Session
from repository.schema import SchemaRepository
from pandas import DataFrame
from io import StringIO
from uuid import uuid4 as uuid


class TransformerService():
    def __init__(self, db: Session, session):
        self.db = db
        self.schemaRepo = SchemaRepository(db, session)
        self.session = session
        self.org_id = session["org_id"]

    def transform(self, df: DataFrame, schema):
        transform = schema["transform"]
        csv_buffer = StringIO()
        if transform == "xlsx":
            output = df.to_excel(csv_buffer, index=False)
        elif transform == "csv":
            output = df.to_csv(csv_buffer, index=False)
        elif transform == "json":
            output = df.to_json(csv_buffer, index=False)
        elif transform == "html":
            output = df.to_html(csv_buffer, index=False)
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
