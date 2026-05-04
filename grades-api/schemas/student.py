from typing import Optional

from sqlmodel import SQLModel


class StudentCreate(SQLModel):
    name: str


class StudentUpdate(SQLModel):
    name: Optional[str] = None
