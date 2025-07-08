from enum import Enum


class UserType(str, Enum):
    student = "student"
    guardian = "guardian"
    teacher = "teacher"
    administrator = "administrator"
    other = "other"


class OrganizationType(str, Enum):
    academic = "academic"
    competitive = "competitive"
    cultural = "cultural"
    non_profit = "non_profit"
    other = "other"
    political = "political"
    religious = "religious"
    social = "social"
    sports = "sports"

