from model.uploads import UploadsModel as Uploads
from utils.repo import get_group_by_queries, filter_parser
from sqlalchemy.orm import Session


class UploadsRepository():
    def __init__(self, db: Session, session=None):
        if session is None:
            session = {}
        self.db = db
        self.org_id = session.get('org_id', None)

    def findAll(self, filter_by, filter_value, group_by, take, skip):
        query = self.db.query(Uploads)

        if (self.org_id is not None):
            query = query.filter(Uploads.org_id == self.org_id)

        if (filter_by is not None and filter_value is not None):
            query = filter_parser(query, Uploads, {
                                  filter_by: filter_value})
        if (take is not None):
            query = query.limit(take)

        if (skip is not None):
            query = query.offset(skip)

        if (group_by is not None):
            return get_group_by_queries(query, Uploads, group_by)
        return query.all()

    def findOne(self, pk):
        query = self.db.query(Uploads).filter(Uploads.id == pk)
        return query.first()

    def create(self, data):
        data['org_id'] = self.org_id
        org = Uploads(**data)
        self.db.add(org)
        self.db.commit()
        return org.id

    def update(self, pk, customer):
        customer['org_id'] = self.org_id
        self.db.query(Uploads).filter(
            Uploads.id == pk).update(customer)
        self.db.commit()
        return "ok"

    def delete(self, pk):
        self.db.query(Uploads).filter(Uploads.id == pk,
                                      Uploads.org_id == self.org_id).delete()
        self.db.commit()
        return "ok"

    def count(self):
        query = self.db.query(Uploads).filter(Uploads.org_id == self.org_id)
        return query.count()
