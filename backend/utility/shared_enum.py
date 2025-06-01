from enum import Enum


class UserType(str, Enum):
    student = "student"
    guardian = "guardian"
    teacher = "teacher"
    administrator = "administrator"
    other = "other"