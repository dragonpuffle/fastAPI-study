from typing import Annotated

from pydantic import BaseModel, BeforeValidator, EmailStr, Field, PositiveFloat, PositiveInt, field_validator


class User(BaseModel):
    name: str
    id: int


class UserAge(BaseModel):
    name: str
    age: int


class FakeUser(BaseModel):
    username: str
    user_info: str


class Feedback(BaseModel):
    name: str
    message: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int | None = None
    is_subscribed: bool | None = None


class Product(BaseModel):
    product_id: PositiveInt = Field("id of the product")
    name: str = Field("name of the product")
    category: str = Field("category of the product")
    price: PositiveFloat = Field("price of the product")


class UserAuth(BaseModel):
    username: str
    password: str
    session_token: int | None = None


class CommonMsg(BaseModel):
    msg: str


class UserA(BaseModel):
    username: str
    password: str


class ContactSchema(BaseModel):
    email: EmailStr
    number: int | None = None


def validmsg(msg: str):
    if len(msg) < 10:
        raise ValueError("String should have at least 10 characters")
    if len(msg) > 50:
        raise ValueError("String should have maximum 50 characters")
    ban_words = ["редиск", "бяк", "козявк"]

    for ban_word in ban_words:
        if ban_word in msg:
            raise ValueError("Use of ban words")

    return msg


Validmsgdep = Annotated[str, BeforeValidator(validmsg)]


class FeedbackValidSchema(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    message: Validmsgdep
    contact: ContactSchema

    @field_validator("name")
    def validata_name(cls, name):
        ban_words = ["редиск", "бяк", "козявк"]

        for ban_word in ban_words:
            if ban_word in name:
                raise ValueError("Use of ban words")

        return name
