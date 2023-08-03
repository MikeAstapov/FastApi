from uuid import uuid4

from fastapi import FastAPI, Form, HTTPException, Cookie, Depends
from fastapi.responses import JSONResponse

from auth import auth_user
from models import Feedback, UserCreate, UserAuth
from products import sample_products

app = FastAPI()

feedback_list = []

# Имитация БД юзеров
users_db = {"admin": "123",
            "user": "321"}

# Имитация БД сессий юзеров
session_db = {}

fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
    3: {"username": "Mike_Astapov", "email": "mike@example.com"},
}


@app.get("/users/{user_id}")
def read_user(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    return {'error': "User not found"}


@app.get('/users')
def read_users(limit: int = 10):
    return dict(list(fake_users.items())[:limit])


@app.post('/feedback')
async def post_feedback(feedback: Feedback):
    feedback_dict = feedback.dict()
    feedback_list.append(feedback_dict)
    return {"message": f"Feedback received. Thank you, {feedback_dict['name']}!"}


@app.get('/feedback')
async def get_feedback():
    return feedback_list


@app.post('/create_user')
async def create_user(user_create: UserCreate):
    return user_create


@app.get('/product/{product_id}')
async def read_product(product_id: int):
    for product in sample_products:
        # Если идентификатор продукта совпадает с переданным в функцию, то возвращаем информацию о продукте
        if product['product_id'] == product_id:
            return product
    return {'Error': "Product not found"}


# Поиск по товарам
@app.get('/products/search')
async def product_search(keyword: str, category: str = None, limit: int = 10):
    # Создаем пустой список для хранения найденных продуктов
    matches_products = []
    for product in sample_products:
        # Проверяем, содержит ли название продукта введенное через keyword слово
        if keyword.lower() in product['name'].lower() and \
                ((not category and category != '') or (category and category.lower() == product['category'].lower())):
            # Добавляем продукт в список найденных продуктов
            matches_products.append(product)
            if len(matches_products) == limit:
                break
    return matches_products


# авторизация по логин\паролю с присвоением куков на 24часа
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username not in users_db or users_db[username] != password:
        raise HTTPException(status_code=400, detail='Неверное имя пользователя или пароль')

    # Генерируем уникальный токен для сессии
    session_token = str(uuid4())
    session_db[session_token] = username

    # Устанавливаем безопасный cookie "session_token"
    responce = JSONResponse(content={"message": "Успешный вход в систему"})
    responce.set_cookie(key='session_token', value=session_token, httponly=True, secure=True, max_age=86400)
    print(session_db)
    return responce


@app.get("/user")
async def get_user_with_coockie(session_token: str = Cookie(None)):
    # Проверяем, есть ли session_token в cookie или он None
    if session_token is None or session_token not in session_db or session_db[session_token] not in users_db:
        # Если session_token отсутствует -401 ошибка
        # Проверяем, есть ли session_token в базе данных сессий и пользователь в базе данных пользователей
        # Если session_token отсутствует в бд сессий или пользователь отсутствует в базе данных пользователей
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    username = session_db[session_token]
    return {'username': username}


@app.get('/login')
async def get_user_auth(user: UserAuth = Depends(auth_user)):
    return {"message": "You got my secret, welcome", "user_info": user.username}
