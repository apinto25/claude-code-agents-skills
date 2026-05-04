from typing import Optional

from sqlmodel import Field, SQLModel

from schemas.grade import Subject


class Grade(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    subject: Subject
    grade: float = Field(ge=0, le=10)
