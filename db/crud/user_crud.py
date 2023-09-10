from sqlalchemy import select

from db.crud.base_crud import BaseCRUD
from db.database import async_session_maker
from db.models import Users


class UserCRUD(BaseCRUD):
    model = Users

    @classmethod
    async def read_user(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(Users.user_id).where(user_id=user_id)
            result = await session.execute(query)
            return result.one_or_none()

    @classmethod
    async def get_all_by_user_id(cls):
        async with async_session_maker() as session:
            query = select(Users.user_id)
            result = await session.execute(query)
            return result.all()
