from pydantic import BaseModel
from typing import Optional


class Info(BaseModel):
    name: str
    inst_name: str
    course_name: str
    annual_income: int
    community: str
    user_id: int


class User(BaseModel):
    name: str
    email: str
    password: str


class showUser(BaseModel):
    name: str
    id: int

    class Config:
        from_attrs = True


# class ShowInfo(BaseModel):
#     name: str
#     inst_name: str
#     course_name: str
#     annual_income: str
#     community: str
#     app_no: str

#     class Config:
#         from_attrs = True


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
