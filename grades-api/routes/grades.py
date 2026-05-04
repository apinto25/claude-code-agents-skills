from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models.grade import Grade
from models.student import Student
from schemas.grade import GradeCreate, GradeUpdate, Subject

router = APIRouter(prefix="/grades", tags=["grades"])


@router.post("", response_model=Grade, status_code=201)
def create_grade(grade: GradeCreate, session: Session = Depends(get_session)):
    if not session.get(Student, grade.student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    db_grade = Grade.model_validate(grade)
    session.add(db_grade)
    session.commit()
    session.refresh(db_grade)
    return db_grade


@router.get("", response_model=list[Grade])
def list_grades(
    student_id: Optional[int] = None,
    subject: Optional[Subject] = None,
    session: Session = Depends(get_session),
):
    query = select(Grade)
    if student_id:
        query = query.where(Grade.student_id == student_id)
    if subject:
        query = query.where(Grade.subject == subject)
    return session.exec(query).all()


@router.get("/{grade_id}", response_model=Grade)
def get_grade(grade_id: int, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grade


@router.patch("/{grade_id}", response_model=Grade)
def update_grade(
    grade_id: int, updates: GradeUpdate, session: Session = Depends(get_session)
):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(grade, field, value)
    session.add(grade)
    session.commit()
    session.refresh(grade)
    return grade


@router.delete("/{grade_id}", status_code=204)
def delete_grade(grade_id: int, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    session.delete(grade)
    session.commit()
