from db.crud import BaseCRUD
from db.models import Users
from db.models.date_time_model import SchDate, SchTime


class DateCRUD(BaseCRUD):
    model = SchDate


class TimeCRUD(BaseCRUD):
    model = SchTime


class UserCRUD(BaseCRUD):
    model = Users

