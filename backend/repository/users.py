from model.users import UserModel as User, UserRole
from sqlalchemy.orm import Session
from utils.repo import get_group_by_queries
from utils.filter_parser import FilterParser
import traceback


class UserRepository():
    def __init__(self, db: Session, session=None):
        if session is None:
            session = {}
        self.db = db
        self.org_id = session.get('org_id', None)

    def findOne(self, user_id: int):
        return self.db.query(User).filter(User.org_id == self.org_id, User.id == user_id).first()

    def findByEmail(self, email: str):
        if self.org_id is None:
            return self.db.query(User).filter(User.email == email).first().__dict__
        else:
            return self.db.query(User).filter(User.org_id == self.org_id, User.email == email).first().__dict__

    def findAll(self, filters, group_by, take, skip):
        try:
            query = self.db.query(User).filter(User.org_id == self.org_id)
            if (filters is not None):
                query = query.filter(
                    *FilterParser(User).parse_filters(filters))

            if (take is not None):
                query = query.limit(take)

            if (skip is not None):
                query = query.offset(skip)

            if (group_by is not None):
                return get_group_by_queries(query, User, group_by)
            return query.all()
        except Exception as e:
            print(traceback.format_exc())

    def create(self, data):
        data['org_id'] = self.org_id
        user = User(**data)
        self.db.add(user)
        self.db.commit()
        return user

    def update(self, pk, user):
        self.db.query(User).filter(
            User.org_id == self.org_id, User.id == pk).update(user)
        self.db.commit()
        return user

    def delete(self, user_id):
        self.db.query(User).filter(User.id == user_id).delete()
        self.db.commit()
        return user_id

    def count(self, filters=None):
        query = self.db.query(User).filter(User.org_id == self.org_id)
        if (filters is not None):
            query = query.filter(
                *FilterParser(User).parse_filters(filters))

        return query.count()

    def updateByEmail(self, email, user):
        self.db.query(User).filter(User.org_id == self.org_id,
                                   User.email == email).update(user)
        self.db.commit()
        return user

    def getRoles(self):
        forward_lookup = [{"id": e.value, "name": e.name} for e in UserRole]
        return {
            "hits": forward_lookup
        }
