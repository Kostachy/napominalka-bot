from sqlalchemy import delete, insert, select, update

from db.database import async_session_maker
from db.models.model import Users


class UserCRUD:

    @classmethod
    async def create_user(cls, **data):
        async with async_session_maker() as session:
            query = insert(Users).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def read_user(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(Users.user_id).filter_by(user_id=user_id)
            result = await session.execute(query)
            return result.one_or_none()

    @classmethod
    async def update_user(cls, **data):
        async with async_session_maker() as session:
            query = update(Users).filter_by(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_user(cls, **filter_by):
        async with async_session_maker() as session:
            query = update(Users).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def get_all_by_user_id(cls):
        async with async_session_maker() as session:
            query = select(Users.user_id)
            result = await session.execute(query)
            return result.all()
