from sqlmodel import Session, select

from models.student import Student


class TestStudentModel:
    def test_create_and_persist(self, session: Session):
        student = Student(name="Alice")
        session.add(student)
        session.commit()
        session.refresh(student)
        assert student.id is not None
        assert student.name == "Alice"

    def test_id_is_auto_assigned(self, session: Session):
        s1 = Student(name="Alice")
        s2 = Student(name="Bob")
        session.add(s1)
        session.add(s2)
        session.commit()
        session.refresh(s1)
        session.refresh(s2)
        assert s1.id != s2.id

    def test_retrieve_by_id(self, session: Session):
        student = Student(name="Alice")
        session.add(student)
        session.commit()
        session.refresh(student)
        fetched = session.get(Student, student.id)
        assert fetched is not None
        assert fetched.name == "Alice"

    def test_update_name(self, session: Session):
        student = Student(name="Alice")
        session.add(student)
        session.commit()
        session.refresh(student)
        student.name = "Bob"
        session.add(student)
        session.commit()
        session.refresh(student)
        assert student.name == "Bob"

    def test_delete(self, session: Session):
        student = Student(name="Alice")
        session.add(student)
        session.commit()
        session.refresh(student)
        student_id = student.id
        session.delete(student)
        session.commit()
        assert session.get(Student, student_id) is None

    def test_list_all(self, session: Session):
        session.add(Student(name="Alice"))
        session.add(Student(name="Bob"))
        session.commit()
        results = session.exec(select(Student)).all()
        assert len(results) == 2
