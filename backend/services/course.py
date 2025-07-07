from fastapi import Depends
from sqlalchemy import Enum, select
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


class CourseService:
    _session: Session

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    def get_all_courses(self) -> list[Course]:

        query = select(CourseEntity)
        result = self._session.scalars(query).all()
        return [course.to_entity() for course in result]

    def get_course_by_id(self, course_id: int) -> Course:

        course = (
            self._session.query(CourseEntity)
            .where(CourseEntity.id == course_id)
            .one_or_none()
        )

        if not course:
            raise ResourceNotFoundException(f"Course with ID {course_id} not found.")
        return course.to_entity()

    def get_course_by_name(self, name: str) -> Course:
        course = (
            self._session.query(CourseEntity)
            .where(CourseEntity.name == name)
            .one_or_none()
        )

        if not course:
            raise ResourceNotFoundException(f"Course with name '{name}' not found.")
        return course.to_entity()

    def get_courses_by_lecturer(self, lecturer: UserEntity) -> list[Course]:
        query = select(CourseEntity).where(CourseEntity.course_lecturer == lecturer)
        result = self._session.scalars(query).all()

        if not result:
            raise ResourceNotFoundException(
                f"No courses found for lecturer {lecturer.id}."
            )
        return [course.to_entity() for course in result]

    def get_course_by_code(self, code: str) -> Course:
        course = (
            self._session.query(CourseEntity)
            .where(CourseEntity.course_code == code)
            .one_or_none()
        )

        if not course:
            raise ResourceNotFoundException(f"Course with code '{code}' not found.")
        return course.to_entity()

    def get_courses_by_credit(self, credit: int) -> list[Course]:
        query = select(CourseEntity).where(CourseEntity.credits == credit)
        result = self._session.scalars(query).all()

        if not result:
            raise ResourceNotFoundException(f"No courses found with {credit} credits.")
        return [course.to_entity() for course in result]

    def get_courses_by_semester(self, semester: str) -> list[Course]:

        query = select(CourseEntity).where(CourseEntity.semester == semester)
        result = self._session.scalars(query).all()

        if not result:
            raise ResourceNotFoundException(
                f"No courses found for semester '{semester}'."
            )
        return [course.to_entity() for course in result]

    def get_courses_by_location(self, location: str) -> list[Course]:
        query = select(CourseEntity).where(CourseEntity.location == location)
        result = self._session.scalars(query).all()

        if not result:
            raise ResourceNotFoundException(
                f"No courses found at location '{location}'."
            )

        return [course.to_entity() for course in result]

    def get_courses_by_department_id(self, department_id: int) -> list[Course]:
        query = select(CourseEntity).where(CourseEntity.department_id == department_id)
        result = self._session.scalars(query).all()
        return [course.to_entity() for course in result]

    def get_courses_by_course_type(self, course_type: str) -> list[Course]:
        query = select(CourseEntity).where(CourseEntity.course_type == course_type)
        result = self._session.scalars(query).all()
        if not result:
            raise ResourceNotFoundException(
                f"No courses found with type '{course_type}'."
            )
        return [course.to_entity() for course in result]

    def get_courses_by_prerequisites(self, prerequisite: list[str]) -> list[Course]:
        query = select(CourseEntity).where(CourseEntity.prerequisites.in_(prerequisite))
        result = self._session.scalars(query).all()
        if not result:
            raise ResourceNotFoundException(
                f"No courses found with prerequisites '{prerequisite}'."
            )
        return [course.to_entity() for course in result]

    def get_courses_by_time(self, time: CourseTime) -> list[Course]:
        query = select(CourseEntity).where(
            CourseEntity.course_time.day == time.day,
            CourseEntity.course_time.start_time <= time.start_time,
            CourseEntity.course_time.end_time >= time.end_time,
        )
        result = self._session.scalars(query).all()
        if not result:
            raise ResourceNotFoundException(f"No courses found at given time.")
        return [course.to_entity() for course in result]

    def create_course(self, course: Course) -> Course:
        existing_course = (
            self._session.query(CourseEntity)
            .filter(CourseEntity.name == course.name)
            .one_or_none()
        )

        if existing_course:
            raise ResourceExistsException(
                f"Course with name '{course.name}' already exists."
            )

        course_entity = CourseEntity.from_model(course)
        self._session.add(course_entity)
        self._session.commit()

        return course_entity.to_model()

    def update_course(self, course_id: int, course: Course) -> Course:
        existing_course = self._session.get(CourseEntity, course_id)

        if not existing_course:
            raise ResourceNotFoundException(f"Course with ID {course_id} not found.")

        # Update the course entity with new values
        for key, value in course.dict(exclude_unset=True).items():
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
