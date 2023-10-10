from repository.schema import SchemaRepository
from sqlalchemy.orm import Session


class SchemaService(SchemaRepository):
    def __init__(self, db: Session, session=None):
        if session is None:
            session = {}
        self.db = db
        self.org_id = session.get('org_id')
        super().__init__(db, session)

    def findAll(self, filters, group_by, take, skip):
        return super().findAll(filters, group_by, take, skip)

    def findOne(self, pk):
        return super().findOne(pk)

    def findOneWithUserId(self, pk):
        return super().findOneWithUserId(pk)

    def create(self, data):
        data = super().create(data)
        return data

    def update(self, pk, data):
        data = super().update(pk, data)
        return data

    def delete(self, pk):
        data = super().delete(pk)
        return data

    def count(self, filter):
        return super().count(filter)
