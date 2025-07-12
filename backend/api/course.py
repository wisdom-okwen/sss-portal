from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from ..models.course import Course, CourseTime
from ..services.course import CourseService
from ..services.exceptions import ResourceNotFoundException, ResourceExistsException

api = APIRouter(prefix="/api/courses", tags=["Courses"])
openapi_tags = {
    "name": "Courses",
    "description": "Course management and related operations.",
}


@api.get("", response_model=List[Course])
def get_all_courses(course_service: CourseService = Depends()) -> List[Course]:
    return course_service.get_all_courses()


@api.get(
    "/{course_id}",
    response_model=Course,
    responses={404: {"description": "Course not found"}},
)
def get_course_by_id(
    course_id: int, course_service: CourseService = Depends()
) -> Course:
    try:
        return course_service.get_course_by_id(course_id)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get(
    "/by_name/{name}",
    response_model=Course,
    responses={404: {"description": "Course not found"}},
)
def get_course_by_name(name: str, course_service: CourseService = Depends()) -> Course:
    try:
        return course_service.get_course_by_name(name)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get("/by_lecturer/{lecturer_id}", response_model=List[Course])
def get_courses_by_lecturer(
    lecturer_id: int, course_service: CourseService = Depends()
) -> List[Course]:
    try:
        return course_service.get_courses_by_lecturer(lecturer_id)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get(
    "/by_code/{code}",
    response_model=Course,
    responses={404: {"description": "Course not found"}},
)
def get_course_by_code(code: str, course_service: CourseService = Depends()) -> Course:
    try:
        return course_service.get_course_by_code(code)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get("/by_credit/{credit}", response_model=List[Course])
def get_courses_by_credit(
    credit: int, course_service: CourseService = Depends()
) -> List[Course]:
    try:
        return course_service.get_courses_by_credit(credit)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get("/by_semester/{semester}", response_model=List[Course])
def get_courses_by_semester(
    semester: str, course_service: CourseService = Depends()
) -> List[Course]:
    try:
        return course_service.get_courses_by_semester(semester)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get("/by_location/{location}", response_model=List[Course])
def get_courses_by_location(
    location: str, course_service: CourseService = Depends()
) -> List[Course]:
    try:
        return course_service.get_courses_by_location(location)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get("/by_department/{department_id}", response_model=List[Course])
def get_courses_by_department_id(
    department_id: int, course_service: CourseService = Depends()
) -> List[Course]:
    return course_service.get_courses_by_department_id(department_id)


@api.get("/by_type/{course_type}", response_model=List[Course])
def get_courses_by_course_type(
    course_type: str, course_service: CourseService = Depends()
) -> List[Course]:
    try:
        return course_service.get_courses_by_course_type(course_type)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get("/by_prerequisites/", response_model=List[Course])
def get_courses_by_prerequisites(
    prerequisite: List[int] = Query([]),  # <-- integers, not strings
    course_service: CourseService = Depends(),
) -> List[Course]:
    try:
        return course_service.get_courses_by_prerequisites(prerequisite)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get("/by_time/", response_model=List[Course])
def get_courses_by_time(
    day: str = Query(..., description="Day of the week"),
    start_time: str = Query(..., description="Start time (HH:MM)"),
    end_time: str = Query(..., description="End time (HH:MM)"),
    course_service: CourseService = Depends(),
) -> List[Course]:
    try:
        course_time = CourseTime(
            day=day,
            start_time=start_time,
            end_time=end_time,
        )
        return course_service.get_courses_by_time(course_time)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.post(
    "",
    response_model=Course,
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "Course already exists"}},
)
def create_course(course: Course, course_service: CourseService = Depends()) -> Course:
    try:
        return course_service.create_course(course)
    except ResourceExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))


@api.put(
    "/{course_id}",
    response_model=Course,
    responses={404: {"description": "Course not found"}},
)
def update_course(
    course_id: int, course: Course, course_service: CourseService = Depends()
) -> Course:
    try:
        return course_service.update_course(course_id, course)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.delete(
    "/{course_id}",
    response_model=Course,
    responses={404: {"description": "Course not found"}},
)
def delete_course(course_id: int, course_service: CourseService = Depends()) -> Course:
    try:
        return course_service.delete_course(course_id)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
