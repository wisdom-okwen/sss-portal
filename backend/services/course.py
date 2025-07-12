from backend.utility.shared_enum import UserType
from .user import UserService
from fastapi import Depends
from sqlalchemy import Enum, select
import json
from sqlalchemy.orm import Session
from ..models.course import Course, CourseTime
from ..database import db_session
from ..entities.user import UserEntity
from ..entities.course import CourseEntity
from .exceptions import (
    UserPermissionException,
    ResourceNotFoundException,
    ResourceExistsException,
)
from backend.models import course
from datetime import time as dt_time


class CourseService:
    _session: Session

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    def get_all_courses(self) -> list[Course]:

        query = select(CourseEntity)
        result = self._session.scalars(query).all()
        return [course.to_model() for course in result]

    def get_course_by_id(self, course_id: int) -> Course:

        course = (
            self._session.query(CourseEntity)
            .where(CourseEntity.id == course_id)
            .one_or_none()
        )

        if not course:
            raise ResourceNotFoundException(f"Course with ID {course_id} not found.")
        return course.to_model()

    def get_course_by_name(self, name: str) -> Course:
        course = (
            self._session.query(CourseEntity)
            .where(CourseEntity.course_name == name)
            .one_or_none()
        )

        if not course:
            raise ResourceNotFoundException(f"Course with name '{name}' not found.")
        return course.to_model()

    def get_courses_by_lecturer(self, lecturer: UserEntity) -> list[Course]:
        query = select(CourseEntity).where(CourseEntity.course_lecturer_id == lecturer)
        result = self._session.scalars(query).all()

        if not result:
            raise ResourceNotFoundException(
                f"No courses found for lecturer {lecturer}."
            )
        return [course.to_model() for course in result]

    def get_course_by_code(self, code: str) -> Course:
        course = (
            self._session.query(CourseEntity)
            .where(CourseEntity.course_code == code)
            .one_or_none()
        )

        if not course:
            raise ResourceNotFoundException(f"Course with code '{code}' not found.")
        return course.to_model()

    def get_courses_by_credit(self, credit: int) -> list[Course]:
        query = select(CourseEntity).where(CourseEntity.credits == credit)
        result = self._session.scalars(query).all()

        if not result:
            raise ResourceNotFoundException(f"No courses found with {credit} credits.")
        return [course.to_model() for course in result]

    def get_courses_by_semester(self, semester: str) -> list[Course]:

        query = select(CourseEntity).where(CourseEntity.semester == semester)
        result = self._session.scalars(query).all()

        if not result:
            raise ResourceNotFoundException(
                f"No courses found for semester '{semester}'."
            )
        return [course.to_model() for course in result]

    def get_courses_by_location(self, location: str) -> list[Course]:
        query = select(CourseEntity).where(CourseEntity.location == location)
        result = self._session.scalars(query).all()

        if not result:
            raise ResourceNotFoundException(
                f"No courses found at location '{location}'."
            )

        return [course.to_model() for course in result]

    def get_courses_by_department_id(self, department_id: int) -> list[Course]:
        query = select(CourseEntity).where(CourseEntity.department_id == department_id)
        result = self._session.scalars(query).all()

        if not result:
            raise ResourceNotFoundException(
                f"No courses found for department ID {department_id}."
            )
        return [course.to_model() for course in result]

    def get_courses_by_course_type(self, course_type: str) -> list[Course]:
        query = select(CourseEntity).where(CourseEntity.course_type == course_type)
        result = self._session.scalars(query).all()
        if not result:
            raise ResourceNotFoundException(
                f"No courses found with type '{course_type}'."
            )
        return [course.to_model() for course in result]

    def get_courses_by_prerequisites(self, prerequisite: list[int]) -> list[Course]:
        query = select(CourseEntity).where(
            CourseEntity.prerequisites.overlap(prerequisite)
        )
        result = self._session.scalars(query).all()
        if not result:
            raise ResourceNotFoundException(
                f"No courses found with prerequisites '{prerequisite}'."
            )
        return [course.to_model() for course in result]

    def get_courses_by_time(self, time: CourseTime) -> list[Course]:

        courses = self._session.query(CourseEntity).all()
        filtered = []
        for course in courses:
            times = json.loads(course.course_time)
            for t in times:
                # Convert string times to datetime.time objects
                t_start = dt_time.fromisoformat(t["start_time"])
                t_end = dt_time.fromisoformat(t["end_time"])
                if (
                    t["day"] == time.day
                    and t_start >= time.start_time
                    and t_end <= time.end_time
                ):
                    filtered.append(course.to_model())
                    break
        if not filtered:
            raise ResourceNotFoundException("No courses found at given time.")
        return filtered

    def create_course(self, course: Course) -> Course:
        existing_course = (
            self._session.query(CourseEntity)
            .where(
                (CourseEntity.course_name == course.course_name)
                | (CourseEntity.course_code == course.course_code)
            )
            .one_or_none()
        )

        if existing_course:
            if existing_course.course_name == course.course_name:
                raise ResourceExistsException(
                    f"Course with name '{course.course_name}' already exists."
                )
            if existing_course.course_code == course.course_code:
                raise ResourceExistsException(
                    f"Course with code '{course.course_code}' already exists."
                )

        user_service = UserService(self._session)
        lecturer = user_service.get_user(course.course_lecturer)
        if not (
            lecturer.user_type == UserType.teacher
            or lecturer.user_type == UserType.administrator
        ):
            raise UserPermissionException(
                "course assignment", f"course with ID {course.id} to user {lecturer.id}"
            )
        course_entity = CourseEntity.from_model(course)
        self._session.add(course_entity)
        self._session.commit()

        return course_entity.to_model()

    def update_course(self, course_id: int, course: Course) -> Course:
        existing_course = self._session.get(CourseEntity, course_id)

        if not existing_course:
            raise ResourceNotFoundException(f"Course with ID {course_id} not found.")

        update_data = course.dict(exclude_unset=True)
        if "course_time" in update_data:

            def serialize_course_time(ct):  # type: ignore
                d = ct.dict() if hasattr(ct, "dict") else dict(ct)
                if hasattr(d["start_time"], "strftime"):
                    d["start_time"] = d["start_time"].strftime("%H:%M:%S")
                if hasattr(d["end_time"], "strftime"):
                    d["end_time"] = d["end_time"].strftime("%H:%M:%S")
                return d

            update_data["course_time"] = json.dumps(
                [serialize_course_time(ct) for ct in update_data["course_time"]]
            )

        # Update the course entity with new values
        for key, value in update_data.items():
            setattr(existing_course, key, value)

        self._session.commit()
        return existing_course.to_model()

    def delete_course(self, course_id: int) -> None:
        course = (
            self._session.query(CourseEntity)
            .where(CourseEntity.id == course_id)
            .one_or_none()
        )

        if not course:
            raise ResourceNotFoundException(f"Course with ID {course_id} not found.")

        self._session.delete(course)
        self._session.commit()

        return course.to_model()
