from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False, index=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    eye_color: Mapped[str] = mapped_column(String, nullable=False)

