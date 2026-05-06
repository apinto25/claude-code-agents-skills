import pytest
from pydantic import ValidationError

from schemas.grade import GradeCreate, GradeUpdate, Subject


class TestSubject:
    def test_valid_values(self):
        assert Subject.math == "math"
        assert Subject.spanish == "spanish"

    def test_invalid_value_raises(self):
        with pytest.raises(ValueError):
            Subject("science")


class TestGradeCreate:
    def test_valid(self):
        g = GradeCreate(student_id=1, subject=Subject.math, grade=7.5)
        assert g.grade == 7.5
        assert g.subject == Subject.math

    def test_grade_at_minimum(self):
        g = GradeCreate(student_id=1, subject=Subject.math, grade=0)
        assert g.grade == 0

    def test_grade_at_maximum(self):
        g = GradeCreate(student_id=1, subject=Subject.math, grade=10)
        assert g.grade == 10

    def test_grade_below_minimum_raises(self):
        with pytest.raises(ValidationError):
            GradeCreate(student_id=1, subject=Subject.math, grade=-0.1)

    def test_grade_above_maximum_raises(self):
        with pytest.raises(ValidationError):
            GradeCreate(student_id=1, subject=Subject.math, grade=10.1)

    def test_student_id_required(self):
        with pytest.raises(ValidationError):
            GradeCreate(subject=Subject.math, grade=5.0)

    def test_subject_required(self):
        with pytest.raises(ValidationError):
            GradeCreate(student_id=1, grade=5.0)

    def test_invalid_subject_raises(self):
        with pytest.raises(ValidationError):
            GradeCreate(student_id=1, subject="science", grade=5.0)


class TestGradeUpdate:
    def test_all_fields_optional(self):
        g = GradeUpdate()
        assert g.subject is None
        assert g.grade is None

    def test_grade_below_minimum_raises(self):
        with pytest.raises(ValidationError):
            GradeUpdate(grade=-0.1)

    def test_grade_above_maximum_raises(self):
        with pytest.raises(ValidationError):
            GradeUpdate(grade=10.1)
