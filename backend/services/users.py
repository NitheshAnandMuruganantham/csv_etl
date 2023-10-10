from repository.users import UserRepository
from fastapi import HTTPException
from services.auth import AuthService


class UserService(UserRepository):
    def __init__(self, db, session):
        self.db = db
        print(session)
        self.user_id = session['org_id']
        self.user_role = session['role']
        super().__init__(db)


    def findAll(self, filters, group_by, take, skip):
        if filters is None:
            filters = {}
        filters['id__ne'] = self.user_id
        return super().findAll(filters, group_by, take, skip)

    def findOne(self, pk):
        return super().findOne(pk)

    def create(self, data):
        data = AuthService(self.db).inviteUser(data)
        return data

    def update(self, pk, data):
        if self.user_id == pk:
            raise HTTPException(403, "You can't update yourself")
        data = super().update(pk, data)
        return data

    def delete(self, pk):
        if self.user_id == pk:
            raise HTTPException(403, "You can't delete yourself")
        data = super().delete(pk)
        return data

    def count(self, filter):
        return super().count(filter)


    def getRoles(self):
        return super().getRoles()
