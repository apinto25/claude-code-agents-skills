from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models.grade import Grade
from models.student import Student
from schemas.student import StudentCreate, StudentUpdate

router = APIRouter(prefix="/students", tags=["students"])


@router.post("", response_model=Student, status_code=201)
def create_student(student: StudentCreate, session: Session = Depends(get_session)):
    db_student = Student.model_validate(student)
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student


@router.get("", response_model=list[Student])
def list_students(session: Session = Depends(get_session)):
    return session.exec(select(Student)).all()


@router.get("/{student_id}", response_model=Student)
def get_student(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.patch("/{student_id}", response_model=Student)
def update_student(
    student_id: int, updates: StudentUpdate, session: Session = Depends(get_session)
):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(student, field, value)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    session.delete(student)
    session.commit()


@router.get("/{student_id}/summary")
def student_summary(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    grades = session.exec(select(Grade).where(Grade.student_id == student_id)).all()
    by_subject = {g.subject: g.grade for g in grades}
    average = round(sum(g.grade for g in grades) / len(grades), 2) if grades else None
    return {"student": student.name, "grades": by_subject, "average": average}
