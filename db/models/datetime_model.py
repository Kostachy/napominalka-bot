from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class ScheduleDateTime(Base):
    __tablename__ = 'scheduledate'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sch_datetime: Mapped[datetime] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    reminder_text: Mapped[str] = mapped_column(nullable=False)
    job_id: Mapped[str] = mapped_column(nullable=False)

    user = relationship('Users', back_populates="schedule_datetime")

    def __repr__(self):
        return f'id-{self.id}'
