from sqlalchemy import select

from db.crud.base_crud import BaseCRUD
from db.database import fetch_one
from db.models import ScheduleDateTime


class DatetimeCRUD(BaseCRUD):
    model = ScheduleDateTime

    @classmethod
    async def get_job_id(cls, **filter_by):
        query = select(ScheduleDateTime.job_id).filter_by(**filter_by)
        return await fetch_one(query)
