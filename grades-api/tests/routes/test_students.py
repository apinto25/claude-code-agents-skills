from fastapi.testclient import TestClient
from sqlmodel import Session

from models.student import Student


def make_student(session: Session, name: str = "Alice") -> Student:
    student = Student(name=name)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


class TestCreateStudent:
    def test_creates_and_returns_student(self, client: TestClient):
        response = client.post("/students", json={"name": "Alice"})
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Alice"
        assert data["id"] is not None

    def test_missing_name_returns_422(self, client: TestClient):
        response = client.post("/students", json={})
        assert response.status_code == 422


class TestListStudents:
    def test_empty_list(self, client: TestClient):
        response = client.get("/students")
        assert response.status_code == 200
        assert response.json() == []

    def test_returns_all_students(self, client: TestClient, session: Session):
        make_student(session, "Alice")
        make_student(session, "Bob")
        response = client.get("/students")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestGetStudent:
    def test_returns_student(self, client: TestClient, session: Session):
        student = make_student(session)
        response = client.get(f"/students/{student.id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Alice"

    def test_not_found(self, client: TestClient):
        response = client.get("/students/999")
        assert response.status_code == 404


class TestUpdateStudent:
    def test_partial_update(self, client: TestClient, session: Session):
        student = make_student(session)
        response = client.patch(f"/students/{student.id}", json={"name": "Bob"})
        assert response.status_code == 200
        assert response.json()["name"] == "Bob"

    def test_not_found(self, client: TestClient):
        response = client.patch("/students/999", json={"name": "Bob"})
        assert response.status_code == 404


class TestDeleteStudent:
    def test_deletes_student(self, client: TestClient, session: Session):
        student = make_student(session)
        response = client.delete(f"/students/{student.id}")
        assert response.status_code == 204
        assert client.get(f"/students/{student.id}").status_code == 404

    def test_not_found(self, client: TestClient):
        response = client.delete("/students/999")
        assert response.status_code == 404


class TestStudentSummary:
    def test_no_grades_returns_none_average(self, client: TestClient, session: Session):
        student = make_student(session)
        response = client.get(f"/students/{student.id}/summary")
        assert response.status_code == 200
        data = response.json()
        assert data["student"] == "Alice"
        assert data["grades"] == {}
        assert data["average"] is None

    def test_single_grade(self, client: TestClient, session: Session):
        student = make_student(session)
        client.post("/grades", json={"student_id": student.id, "subject": "math", "grade": 8.0})
        response = client.get(f"/students/{student.id}/summary")
        assert response.status_code == 200
        data = response.json()
        assert data["grades"]["math"] == 8.0
        assert data["average"] == 8.0

    def test_multiple_subjects_average(self, client: TestClient, session: Session):
        student = make_student(session)
        client.post("/grades", json={"student_id": student.id, "subject": "math", "grade": 6.0})
        client.post("/grades", json={"student_id": student.id, "subject": "spanish", "grade": 9.0})
        response = client.get(f"/students/{student.id}/summary")
        assert response.status_code == 200
        data = response.json()
        assert data["average"] == 7.5

    def test_not_found(self, client: TestClient):
        response = client.get("/students/999/summary")
        assert response.status_code == 404
