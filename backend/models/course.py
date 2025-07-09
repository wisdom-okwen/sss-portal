from pydantic import BaseModel
from typing import List
from datetime import time
from ..models.user import User


class CourseTime(BaseModel):
    day: str
    start_time: time
    end_time: time


class Course(BaseModel):
    id: int | None = None
    course_name: str = ""
    course_code: str = ""
    course_description: str = ""
    course_lecturer: int | None = None
    course_capacity: int = 0
    course_time: List[CourseTime] = []
    course_members: List[int] = []
    credits: int = 0
    department_id: int | None = None
    prerequisites: List[int] = []
    course_type: str = ""
    num_enrolled: int = 0
    location: str = ""
    semester: str = ""
