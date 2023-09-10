from db.crud.base_crud import BaseCRUD
from db.models import ScheduleDateTime


class DatetimeCRUD(BaseCRUD):
    model = ScheduleDateTime
