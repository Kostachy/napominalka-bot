from sqlalchemy import select

from db.crud.base_crud import BaseCRUD
from db.database import async_session_maker
from db.models import ScheduleDateTime


class DatetimeCRUD(BaseCRUD):
    model = ScheduleDateTime

    @classmethod
    async def get_job_id(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(ScheduleDateTime.job_id).filter_by(**filter_by)
            result = await session.execute(query)
            return result.one_or_none()
