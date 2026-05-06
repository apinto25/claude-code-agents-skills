import pytest
from pydantic import ValidationError

from schemas.student import StudentCreate, StudentUpdate


class TestStudentCreate:
    def test_valid(self):
        s = StudentCreate(name="Alice")
        assert s.name == "Alice"

    def test_name_required(self):
        with pytest.raises(ValidationError):
            StudentCreate()

    def test_name_cannot_be_none(self):
        with pytest.raises(ValidationError):
            StudentCreate(name=None)


class TestStudentUpdate:
    def test_all_fields_optional(self):
        s = StudentUpdate()
        assert s.name is None

    def test_name_can_be_set(self):
        s = StudentUpdate(name="Bob")
        assert s.name == "Bob"
