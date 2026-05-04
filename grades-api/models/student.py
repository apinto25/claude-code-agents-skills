from typing import Optional

from sqlmodel import Field, SQLModel


class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
