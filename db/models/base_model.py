from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from db.database import Base


class Users(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)

    schedule_datetime = relationship('ScheduleDateTime', back_populates="user")

    def __repr__(self):
        return "user_id={}, username={}".format(self.user_id, self.username)
