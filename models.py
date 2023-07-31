from pydantic import BaseModel, EmailStr



class UserRegister(BaseModel):
    name: str
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
