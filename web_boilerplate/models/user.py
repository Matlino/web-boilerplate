from sqlalchemy import Column, Integer, String

from ..db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    age = Column(Integer, nullable=False)
    eye_color = Column(String, nullable=False)

