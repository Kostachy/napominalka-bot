from sqlalchemy import delete, insert, select, update

from db.database import async_session_maker
from db.models.base_model import Users


class BaseCRUD:
    model = None

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def read(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.one_or_none()

    @classmethod
    async def update_user(cls, **data):
        async with async_session_maker() as session:
            query = update(cls.model).filter_by(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_user(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
