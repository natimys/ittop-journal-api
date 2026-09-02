from datetime import date
from enum import IntEnum

from pydantic import BaseModel


class Grade(IntEnum):
    EXCELLENT = 5
    GOOD = 4
    SATISFACTORY = 3
    UNSATISFACTORY = 2


class MonthPoints(BaseModel):
    date: date
    points: Grade | None
    previous_points: Grade | None
    has_rasp: bool | None

