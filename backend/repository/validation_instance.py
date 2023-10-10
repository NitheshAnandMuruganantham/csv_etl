from model.validation_instance import ValidationInstanceModel as Schema
from sqlalchemy.orm import Session
from utils.filter_parser import FilterParser
from utils.repo import get_group_by_queries
from fastapi import HTTPException


class ValidationInstanceRepository():
    def __init__(self, db: Session, session):
        self.db = db
        self.session = session
        self.org_id = session.get('org_id', None)

    def findAll(self, filters=None, group_by=None, take=None, skip=None):
        query = self.db.query(Schema).filter(
            Schema.org_id == self.org_id)

        if (filters is not None):
            query = query.filter(
                *FilterParser(Schema).parse_filters(filters))

        if (take is not None):
            query = query.limit(take)

        if (skip is not None):
            query = query.offset(skip)

        if (group_by is not None):
            return get_group_by_queries(query, Schema, group_by)

        return query.all()

    def findOne(self, pk):
        return self.db.query(Schema).filter(Schema.org_id == self.org_id, Schema.id == pk).first()

    def create(self, data):
        data['org_id'] = self.org_id
        org = Schema(**data)
        self.db.add(org)
        self.db.commit()
        return org

    def update(self, pk, data):
        query = self.db.query(Schema).filter(
            Schema.org_id == self.org_id,
            Schema.id == pk)
        exists = query.first()
        if exists is None:
            raise HTTPException(
                status_code=403, detail="the id does not exists")
        query.update(data)
        self.db.commit()

        return query.first()

    def delete(self, pk):
        query = self.db.query(Schema).filter(
            Schema.org_id == self.org_id, Schema.id == pk)
        if query.first() is None:
            raise HTTPException(
                status_code=403, detail="the id does not exists")
        try:
            query.delete()
        except:
            raise HTTPException(
                status_code=401, detail="related entities exists"
            )
        self.db.commit()
        return "ok"

    def count(self, filters):
        query = self.db.query(Schema).filter(
            Schema.org_id == self.org_id)
        if filters is not None:
            query = query.filter(
                *FilterParser(Schema).parse_filters(filters))
        return query.count()
