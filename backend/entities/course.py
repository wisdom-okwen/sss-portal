from ctypes import ARRAY
from typing import List, Self
from backend.utility.shared_enum import UserType
from sqlalchemy import String, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column
from .base_entity import EntityBase
from backend.models.course import Course, CourseTime


class CourseEntity(EntityBase):

    __tablename__ = "course"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    course_name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, default=""
    )
    course_code: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, default=""
    )
    course_description: Mapped[str] = mapped_column(
        String(500), nullable=True, default=""
    )
    course_lecturer: Mapped[UserType] = mapped_column(
        Enum(UserType), nullable=False, default=None
    )
    course_capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    course_time: Mapped[CourseTime] = mapped_column(
        Enum(CourseTime), nullable=False, default=None
    )
    course_members: Mapped[List[UserType]] = mapped_column(
        ARRAY(Enum(UserType)), nullable=True, default=list
    )
    credits: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    department_id: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
    prerequisites: Mapped[List[int]] = mapped_column(
        ARRAY(Integer), nullable=True, default=list
    )
    course_type: Mapped[str] = mapped_column(String(50), nullable=False, default="")
    num_enrolled: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    location: Mapped[str] = mapped_column(String(255), nullable=True, default="")
    semester: Mapped[str] = mapped_column(String(50), nullable=False, default="")

    def to_model(self) -> Course:
        return Course(
            id=self.id,
            course_name=self.course_name,
            course_code=self.course_code,
            course_description=self.course_description,
            course_lecturer=self.course_lecturer,
            course_capacity=self.course_capacity,
            course_time=self.course_time,
            course_members=self.course_members,
            credits=self.credits,
            department_id=self.department_id,
            prerequisites=self.prerequisites,
            course_type=self.course_type,
            num_enrolled=self.num_enrolled,
            location=self.location,
            semester=self.semester,
        )

    @classmethod
    def from_model(cls, model: Course) -> Self:
        return cls(
            id=model.id,
            course_name=model.course_name,
            course_code=model.course_code,
            course_description=model.course_description,
            course_lecturer=model.course_lecturer,
            course_capacity=model.course_capacity,
            course_time=model.course_time,
            course_members=model.course_members,
            credits=model.credits,
            department_id=model.department_id,
            prerequisites=model.prerequisites,
            course_type=model.course_type,
            num_enrolled=model.num_enrolled,
            location=model.location,
            semester=model.semester,
        )
