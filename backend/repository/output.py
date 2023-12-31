from model.output import OutputModel as Output
from fastapi import HTTPException
from utils.repo import get_group_by_queries
from utils.filter_parser import FilterParser
from sqlalchemy.orm import Session


class OutputRepository():
    def __init__(self, db: Session, session=None):
        if session is None:
            session = {}
        self.db = db
        self.org_id = session.get('org_id', None)

    def findAll(self, filters=None, group_by=None, take=None, skip=None):
        query = self.db.query(Output).filter(
            Output.org_id == self.org_id)

        if (filters is not None):
            query = query.filter(
                *FilterParser(Output).parse_filters(filters))

        if (take is not None):
            query = query.limit(take)

        if (skip is not None):
            query = query.offset(skip)

        if (group_by is not None):
            return get_group_by_queries(query, Output, group_by)

        return query.all()

    def findOne(self, pk):
        return self.db.query(Output).filter(Output.org_id == self.org_id, Output.id == pk).first()

    def findOneWithUserId(self, id):
        query = self.db.query(Output).filter(Output.user_id == id)
        return query.first()

    def create(self, customer):
        customer['org_id'] = self.org_id
        org = Output(**customer)
        self.db.add(org)
        self.db.commit()
        return org

    def update(self, pk, data):
        query = self.db.query(Output).filter(
            Output.org_id == self.org_id,
            Output.id == pk)
        exists = query.first()
        if exists is None:
            raise HTTPException(
                status_code=403, detail="the id does not exists")
        query.update(data)
        self.db.commit()

        return query.first()

    def delete(self, pk):
        query = self.db.query(Output).filter(
            Output.org_id == self.org_id, Output.id == pk)
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
        query = self.db.query(Output).filter(
            Output.org_id == self.org_id)
        if filters is not None:
            query = query.filter(
                *FilterParser(Output).parse_filters(filters))
        return query.count()
