from pydantic import BaseModel, EmailStr, PositiveInt, PositiveFloat, Field


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
    product_id: PositiveInt = Field('id of the product')
    name: str = Field('name of the product')
    category: str = Field('category of the product')
    price: PositiveFloat = Field('price of the product')


class UserAuth(BaseModel):
    username: str
    password: str
    session_token: int | None = None


class CommonMsg(BaseModel):
    msg: str


