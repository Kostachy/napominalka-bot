from typing import Optional

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from db.database import Base


class Users(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return "<id={}, user_id={}, username={}>".format(self.id, self.user_id, self.username)



