from sqlalchemy import String, Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base_entity import EntityBase
from backend.models.course import Course
from typing import List, Self
import json
from sqlalchemy.dialects.postgresql import ARRAY


class CourseEntity(EntityBase):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    course_name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, default=""
    )
    course_code: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, default=""
    )
    course_description: Mapped[str] = mapped_column(
        String(500), nullable=True, default=""
    )
    course_lecturer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=True
    )
    course_capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    course_time: Mapped[str] = mapped_column(String, nullable=True, default="[]")
    course_member_ids: Mapped[List[int]] = mapped_column(
        ARRAY(Integer), nullable=True, default=list
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
            course_lecturer=self.course_lecturer_id,
            course_capacity=self.course_capacity,
            course_time=json.loads(self.course_time),
            course_members=self.course_member_ids,
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
        def serialize_course_time(ct):  # type: ignore
            d = ct.dict()
            if hasattr(d["start_time"], "strftime"):
                d["start_time"] = d["start_time"].strftime("%H:%M:%S")
            if hasattr(d["end_time"], "strftime"):
                d["end_time"] = d["end_time"].strftime("%H:%M:%S")
            return d

        return cls(
            course_name=model.course_name,
            course_code=model.course_code,
            course_description=model.course_description,
            course_lecturer_id=model.course_lecturer,
            course_capacity=model.course_capacity,
            course_time=json.dumps(
                [serialize_course_time(ct) for ct in model.course_time]
            ),
            credits=model.credits,
            department_id=model.department_id,
            prerequisites=model.prerequisites,
            course_type=model.course_type,
            num_enrolled=model.num_enrolled,
            location=model.location,
            semester=model.semester,
        )
