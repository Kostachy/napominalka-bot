from datetime import date,  time
from sqlalchemy import Integer, ForeignKey, Date, Time
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from db.database import Base


class SchDate(Base):
    __tablename__ = "scheduling_date"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    schedule_date: Mapped[date] = mapped_column(Date, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.user_id'), nullable=False)

    def __repr__(self):
        return f'{id}{self.schedule_date}---{self.user_id}---{self.schedule_date}'


class SchTime(Base):
    __tablename__ = "scheduling_time"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    schedule_time: Mapped[time] = mapped_column(Time, nullable=False, unique=True)
    schedule_date: Mapped[date] = mapped_column(Date, ForeignKey('scheduling_date.schedule_date'), nullable=False)
