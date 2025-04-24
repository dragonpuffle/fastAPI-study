from pydantic import BaseModel, EmailStr


class UserLogins(BaseModel):
    username: str
    password: str


class Users(BaseModel):
    username: str
    full_name: str | None = None
    email: EmailStr | None = None
    intro: str | None = None
    roles: list[str]


class Ideas(BaseModel):
    idea: str
    is_done: bool = False
    report: str | None = None
