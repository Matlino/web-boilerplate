from datetime import datetime
from pydantic import BaseModel
from typing import Dict


class UserStatisticsBase(BaseModel):
    total_users: int
    average_age: float
    min_age: int
    max_age: int
    eye_color_distribution: Dict[str, int]
    calculated_at: datetime


class UserStatisticsOut(UserStatisticsBase):
    pass


