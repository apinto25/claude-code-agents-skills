from sqlmodel import Session, select

from models.grade import Grade
from models.student import Student
from schemas.grade import Subject


def make_student(session: Session, name: str = "Alice") -> Student:
    student = Student(name=name)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


class TestGradeModel:
    def test_create_and_persist(self, session: Session):
        student = make_student(session)
        grade = Grade(student_id=student.id, subject=Subject.math, grade=8.0)
        session.add(grade)
        session.commit()
        session.refresh(grade)
        assert grade.id is not None
        assert grade.student_id == student.id
        assert grade.subject == Subject.math
        assert grade.grade == 8.0

    def test_retrieve_by_id(self, session: Session):
        student = make_student(session)
        grade = Grade(student_id=student.id, subject=Subject.spanish, grade=6.5)
        session.add(grade)
        session.commit()
        session.refresh(grade)
        fetched = session.get(Grade, grade.id)
        assert fetched is not None
        assert fetched.grade == 6.5

    def test_update_grade_value(self, session: Session):
        student = make_student(session)
        grade = Grade(student_id=student.id, subject=Subject.math, grade=5.0)
        session.add(grade)
        session.commit()
        session.refresh(grade)
        grade.grade = 9.0
        session.add(grade)
        session.commit()
        session.refresh(grade)
        assert grade.grade == 9.0

    def test_delete(self, session: Session):
        student = make_student(session)
        grade = Grade(student_id=student.id, subject=Subject.math, grade=7.0)
        session.add(grade)
        session.commit()
        session.refresh(grade)
        grade_id = grade.id
        session.delete(grade)
        session.commit()
        assert session.get(Grade, grade_id) is None

    def test_filter_by_student(self, session: Session):
        alice = make_student(session, "Alice")
        bob = make_student(session, "Bob")
        session.add(Grade(student_id=alice.id, subject=Subject.math, grade=7.0))
        session.add(Grade(student_id=bob.id, subject=Subject.math, grade=9.0))
        session.commit()
        results = session.exec(select(Grade).where(Grade.student_id == alice.id)).all()
        assert len(results) == 1
        assert results[0].student_id == alice.id
