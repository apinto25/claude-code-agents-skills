from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class Subject(str, Enum):
    math = "math"
    spanish = "spanish"


class GradeCreate(SQLModel):
    student_id: int
    subject: Subject
    grade: float = Field(ge=0, le=10)


class GradeUpdate(SQLModel):
    subject: Optional[Subject] = None
    grade: Optional[float] = Field(default=None, ge=0, le=10)
