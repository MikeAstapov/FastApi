from pydantic import BaseModel, EmailStr


class UserAuth(BaseModel):
    username: str
    password: str


class Feedback(BaseModel):
    name: str
    message: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int = None
    is_subscribed: bool = True


class Products(BaseModel):
    product_id: int
    name: str
    category: str
    price: float


def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None


USER_DATA = [UserAuth(**{"username": "user1", "password": "pass1"}),
             UserAuth(**{"username": "user2", "password": "pass2"})]
