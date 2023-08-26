from sqlalchemy.orm import Session
from repository.schema import SchemaRepository
from pandas import DataFrame


class CleanUpService():
    def __init__(self, db: Session, session):
        self.db = db
        self.schemaRepo = SchemaRepository(db, session)
        self.session = session
        self.org_id = session["org_id"]

    def cleanup(self, df: DataFrame, schema):
        schema = schema["clean_up"]
        emoji_treatment = schema["emoji_treatment"]
        nan_treatment = schema["nan_treatment"]

        if nan_treatment['action'] == 'drop':
            df.dropna(inplace=True)

        elif nan_treatment['action'] == 'replace':
            for col in nan_treatment['columns']:
                df[col].fillna(nan_treatment['value'], inplace=True)

        if emoji_treatment['action'] == 'drop':
            df.astype(str).apply(lambda x: x.str.encode(
                'ascii', 'ignore').str.decode('ascii'))

        return df
