from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from database import engine
from models import grade, student  # noqa: F401 — registers tables with SQLModel metadata
from routes import grades, students


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="Student Grades API", lifespan=lifespan)
app.include_router(students.router)
app.include_router(grades.router)
