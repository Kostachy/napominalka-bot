from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from db.database import Base


class ScheduleDateTime(Base):
    __tablename__ = 'scheduledate'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sch_datetime: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
