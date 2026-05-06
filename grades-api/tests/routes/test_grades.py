from fastapi.testclient import TestClient
from sqlmodel import Session

from models.student import Student


def make_student(session: Session, name: str = "Alice") -> Student:
    student = Student(name=name)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


class TestCreateGrade:
    def test_creates_and_returns_grade(self, client: TestClient, session: Session):
        student = make_student(session)
        response = client.post(
            "/grades", json={"student_id": student.id, "subject": "math", "grade": 7.5}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["student_id"] == student.id
        assert data["subject"] == "math"
        assert data["grade"] == 7.5

    def test_student_not_found_returns_404(self, client: TestClient):
        response = client.post(
            "/grades", json={"student_id": 999, "subject": "math", "grade": 7.5}
        )
        assert response.status_code == 404

    def test_grade_below_minimum_returns_422(self, client: TestClient, session: Session):
        student = make_student(session)
        response = client.post(
            "/grades", json={"student_id": student.id, "subject": "math", "grade": -0.1}
        )
        assert response.status_code == 422

    def test_grade_above_maximum_returns_422(self, client: TestClient, session: Session):
        student = make_student(session)
        response = client.post(
            "/grades", json={"student_id": student.id, "subject": "math", "grade": 10.1}
        )
        assert response.status_code == 422

    def test_grade_at_boundaries_accepted(self, client: TestClient, session: Session):
        student = make_student(session)
        r1 = client.post(
            "/grades", json={"student_id": student.id, "subject": "math", "grade": 0}
        )
        r2 = client.post(
            "/grades", json={"student_id": student.id, "subject": "spanish", "grade": 10}
        )
        assert r1.status_code == 201
        assert r2.status_code == 201

    def test_invalid_subject_returns_422(self, client: TestClient, session: Session):
        student = make_student(session)
        response = client.post(
            "/grades", json={"student_id": student.id, "subject": "science", "grade": 7.0}
        )
        assert response.status_code == 422


class TestListGrades:
    def test_no_filters_returns_all(self, client: TestClient, session: Session):
        student = make_student(session)
        client.post("/grades", json={"student_id": student.id, "subject": "math", "grade": 5.0})
        client.post("/grades", json={"student_id": student.id, "subject": "spanish", "grade": 8.0})
        response = client.get("/grades")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_filter_by_student_id(self, client: TestClient, session: Session):
        alice = make_student(session, "Alice")
        bob = make_student(session, "Bob")
        client.post("/grades", json={"student_id": alice.id, "subject": "math", "grade": 5.0})
        client.post("/grades", json={"student_id": bob.id, "subject": "math", "grade": 8.0})
        response = client.get(f"/grades?student_id={alice.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["student_id"] == alice.id

    def test_filter_by_subject(self, client: TestClient, session: Session):
        student = make_student(session)
        client.post("/grades", json={"student_id": student.id, "subject": "math", "grade": 5.0})
        client.post("/grades", json={"student_id": student.id, "subject": "spanish", "grade": 8.0})
        response = client.get("/grades?subject=math")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["subject"] == "math"

    def test_filter_by_student_id_and_subject(self, client: TestClient, session: Session):
        alice = make_student(session, "Alice")
        bob = make_student(session, "Bob")
        client.post("/grades", json={"student_id": alice.id, "subject": "math", "grade": 5.0})
        client.post("/grades", json={"student_id": alice.id, "subject": "spanish", "grade": 7.0})
        client.post("/grades", json={"student_id": bob.id, "subject": "math", "grade": 8.0})
        response = client.get(f"/grades?student_id={alice.id}&subject=math")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["student_id"] == alice.id
        assert data[0]["subject"] == "math"


class TestGetGrade:
    def test_returns_grade(self, client: TestClient, session: Session):
        student = make_student(session)
        created = client.post(
            "/grades", json={"student_id": student.id, "subject": "math", "grade": 7.0}
        ).json()
        response = client.get(f"/grades/{created['id']}")
        assert response.status_code == 200
        assert response.json()["grade"] == 7.0

    def test_not_found(self, client: TestClient):
        response = client.get("/grades/999")
        assert response.status_code == 404


class TestUpdateGrade:
    def test_partial_update(self, client: TestClient, session: Session):
        student = make_student(session)
        created = client.post(
            "/grades", json={"student_id": student.id, "subject": "math", "grade": 5.0}
        ).json()
        response = client.patch(f"/grades/{created['id']}", json={"grade": 9.0})
        assert response.status_code == 200
        assert response.json()["grade"] == 9.0

    def test_not_found(self, client: TestClient):
        response = client.patch("/grades/999", json={"grade": 9.0})
        assert response.status_code == 404


class TestDeleteGrade:
    def test_deletes_grade(self, client: TestClient, session: Session):
        student = make_student(session)
        created = client.post(
            "/grades", json={"student_id": student.id, "subject": "math", "grade": 5.0}
        ).json()
        response = client.delete(f"/grades/{created['id']}")
        assert response.status_code == 204
        assert client.get(f"/grades/{created['id']}").status_code == 404

    def test_not_found(self, client: TestClient):
        response = client.delete("/grades/999")
        assert response.status_code == 404
