from sqlalchemy import select

from db.crud.base_crud import BaseCRUD
from db.database import fetch_one, fetch_all
from db.models import Users


class UserCRUD(BaseCRUD):
    model = Users

    @classmethod
    async def read_user(cls, user_id: int):
        query = select(Users.user_id).filter_by(user_id=user_id)
        return await fetch_one(query)

    @classmethod
    async def get_all_by_user_id(cls):
        query = select(Users.user_id)
        return await fetch_all(query)
