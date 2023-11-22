from sqlalchemy import delete, insert, select, update

from db.database import fetch_one, new_execute


class BaseCRUD:
    model = None

    @classmethod
    async def add(cls, **data):
        query = insert(cls.model).values(**data)
        await new_execute(query)

    @classmethod
    async def read(cls, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        return await fetch_one(query)

    @classmethod
    async def update(cls, **data):
        query = update(cls.model).filter_by(**data)
        await new_execute(query)

    @classmethod
    async def delete(cls, **filter_by):
        query = delete(cls.model).filter_by(**filter_by)
        await new_execute(query)
