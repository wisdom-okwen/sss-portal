"""
Mock data for courses.

Ten courses are setup for testing and development purposes.
"""

import pytest
from sqlalchemy.orm import Session
from ..models.course import Course, CourseTime
from ..entities.course import CourseEntity
from .reset_table_id_sequence import reset_table_id_seq

# Example course times for variety
course_times = [
    [CourseTime(day="Monday", start_time="09:00:00", end_time="10:30:00")],
    [CourseTime(day="Tuesday", start_time="11:00:00", end_time="12:30:00")],
    [CourseTime(day="Wednesday", start_time="13:00:00", end_time="14:30:00")],
    [CourseTime(day="Thursday", start_time="15:00:00", end_time="16:30:00")],
    [CourseTime(day="Friday", start_time="10:00:00", end_time="11:30:00")],
    [CourseTime(day="Monday", start_time="14:00:00", end_time="15:30:00")],
    [CourseTime(day="Tuesday", start_time="09:00:00", end_time="10:30:00")],
    [CourseTime(day="Wednesday", start_time="11:00:00", end_time="12:30:00")],
    [CourseTime(day="Thursday", start_time="13:00:00", end_time="14:30:00")],
    [CourseTime(day="Friday", start_time="15:00:00", end_time="16:30:00")],
]

courses = [
    Course(
        id=1,
        course_name="Physics 101",
        course_code="PHY101",
        course_description="Introduction to Physics",
        course_lecturer=4,  # Isaac (teacher)
        course_capacity=30,
        course_time=course_times[0],
        course_members=[1, 2],
        credits=4,
        department_id=1,
        prerequisites=[],
        course_type="core",
        num_enrolled=2,
        location="Room 101",
        semester="Fall",
    ),
    Course(
        id=2,
        course_name="Mathematics 101",
        course_code="MTH101",
        course_description="Calculus I",
        course_lecturer=4,
        course_capacity=40,
        course_time=course_times[1],
        course_members=[1],
        credits=4,
        department_id=2,
        prerequisites=[],
        course_type="core",
        num_enrolled=1,
        location="Room 102",
        semester="Fall",
    ),
    Course(
        id=3,
        course_name="History 201",
        course_code="HIS201",
        course_description="World History",
        course_lecturer=3,  # Armstrong (admin)
        course_capacity=25,
        course_time=course_times[2],
        course_members=[2],
        credits=3,
        department_id=3,
        prerequisites=[1],
        course_type="elective",
        num_enrolled=1,
        location="Room 103",
        semester="Spring",
    ),
    Course(
        id=4,
        course_name="Chemistry 101",
        course_code="CHE101",
        course_description="Basic Chemistry",
        course_lecturer=4,
        course_capacity=35,
        course_time=course_times[3],
        course_members=[1, 3],
        credits=4,
        department_id=1,
        prerequisites=[],
        course_type="core",
        num_enrolled=2,
        location="Lab 1",
        semester="Fall",
    ),
    Course(
        id=5,
        course_name="Biology 101",
        course_code="BIO101",
        course_description="Intro to Biology",
        course_lecturer=4,
        course_capacity=30,
        course_time=course_times[4],
        course_members=[2, 3],
        credits=4,
        department_id=1,
        prerequisites=[],
        course_type="core",
        num_enrolled=2,
        location="Lab 2",
        semester="Spring",
    ),
    Course(
        id=6,
        course_name="Computer Science 101",
        course_code="CSC101",
        course_description="Programming Basics",
        course_lecturer=3,
        course_capacity=50,
        course_time=course_times[5],
        course_members=[1, 2, 3],
        credits=5,
        department_id=4,
        prerequisites=[],
        course_type="core",
        num_enrolled=3,
        location="Comp Lab",
        semester="Fall",
    ),
    Course(
        id=7,
        course_name="English Literature",
        course_code="ENG201",
        course_description="Shakespeare and Beyond",
        course_lecturer=3,
        course_capacity=20,
        course_time=course_times[6],
        course_members=[1],
        credits=3,
        department_id=5,
        prerequisites=[],
        course_type="elective",
        num_enrolled=1,
        location="Room 201",
        semester="Spring",
    ),
    Course(
        id=8,
        course_name="Economics 101",
        course_code="ECO101",
        course_description="Principles of Economics",
        course_lecturer=4,
        course_capacity=40,
        course_time=course_times[7],
        course_members=[2],
        credits=4,
        department_id=6,
        prerequisites=[],
        course_type="core",
        num_enrolled=1,
        location="Room 202",
        semester="Fall",
    ),
    Course(
        id=9,
        course_name="Art History",
        course_code="ART101",
        course_description="Art through the Ages",
        course_lecturer=3,
        course_capacity=15,
        course_time=course_times[8],
        course_members=[3],
        credits=2,
        department_id=7,
        prerequisites=[],
        course_type="elective",
        num_enrolled=1,
        location="Art Studio",
        semester="Spring",
    ),
    Course(
        id=10,
        course_name="Philosophy 101",
        course_code="PHL101",
        course_description="Introduction to Philosophy",
        course_lecturer=4,
        course_capacity=25,
        course_time=course_times[9],
        course_members=[1, 2, 3],
        credits=3,
        department_id=8,
        prerequisites=[2, 3],
        course_type="elective",
        num_enrolled=3,
        location="Room 301",
        semester="Fall",
    ),
]


def insert_fake_course_data(session: Session):
    global courses
    entities = []
    for course in courses:
        entity = CourseEntity.from_model(course)
        session.add(entity)
        entities.append(entity)
    reset_table_id_seq(session, CourseEntity, CourseEntity.id, len(courses) + 1)
    session.commit()  # Commit to ensure Course IDs in database


@pytest.fixture(autouse=True)
def fake_course_data_fixture(session: Session):
    insert_fake_course_data(session)
    session.commit()
    yield
