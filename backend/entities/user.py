from sqlalchemy.orm import Column, String, Integer 

class UserEntity:
    # entity for user table
    __table__ = "user"

    # def __init__(s)