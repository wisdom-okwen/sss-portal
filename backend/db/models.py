from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String(255), nullable=False, unique=True)
    course_code = Column(String(50), nullable=False, unique=True)
    course_description = Column(String(500), nullable=True)
    course_lecturer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    course_capacity = Column(Integer, nullable=False, default=0)
    course_time = Column(String, nullable=True, default="[]")  # Store as JSON string
    course_member_ids = Column(ARRAY(Integer), nullable=True, default=list)
    credits = Column(Integer, nullable=False, default=0)
    department_id = Column(Integer, nullable=True)
    prerequisites = Column(ARRAY(Integer), nullable=True, default=list)
    course_type = Column(String(50), nullable=False, default="")
    num_enrolled = Column(Integer, nullable=False, default=0)
    location = Column(String(255), nullable=True)
    semester = Column(String(50), nullable=False, default="")
