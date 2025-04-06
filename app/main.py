import uuid
from datetime import datetime

from fastapi import BackgroundTasks, Cookie, FastAPI, Form, HTTPException, Response

from app.models import CommonMsg, Feedback, Product, User, UserCreate


# uvicorn main:app --reload
app = FastAPI()
# user = User(**{'name': 'John Doe', 'id': 1})

fake_db = [{"username": "vasya", "user_id": 2}, {"username": "katya", "user_id": 3}]
fake_users = {
    1: {"username": "vasya", "user_info": "balbes"},
    2: {"username": "katya", "user_info": "ne balbes"},
    3: {"username": "andrewa", "user_info": "balbes"},
    4: {"username": "ann", "user_info": "ne balbes"},
    5: {"username": "den", "user_info": "balbes"},
    6: {"username": "roma", "user_info": "ne balbes"},
}
db_cru: list[UserCreate] = []


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.get("/custom")
async def read_custom_message():
    return {"message": "This is a custom message!"}


@app.get("/users")
async def read_user(limit: int = 10):
    return dict(list(fake_users.items())[:limit])


# http://127.0.0.1:8000/users?limit=3


@app.post("/add_user", response_model=User)
async def add_user(user: User):
    fake_db.append({"username": user.name, "user_id": user.id})
    return user


# @app.post('/user')
# async def show_user(usr: UserAge):
#     return {'name': usr.name,
#             'age': usr.age,
#             'isadult': usr.age >= 18}


@app.get("/solve_{num1}_{num2}")
async def calculate_nums(num1: int, num2: int):
    return {"result": calculate(num1, num2)}


def calculate(num1, num2):
    return num1 + num2


@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int):
    return fake_users.get(user_id, {"error": "User not found"})


@app.post("/feedback")
async def save_feedback(feedback: Feedback):
    write_feedback(feedback)
    return {"message": f"Feedback received. Thank you, {feedback.name}!"}


def write_feedback(feedback: Feedback):
    path = "logs.txt"
    with open(path, "a") as logs:
        logs.write(str(feedback))
        logs.write("\n")


@app.post("/create_user", response_model=UserCreate)
async def create_user(user: UserCreate) -> UserCreate:
    db_cru.append(user)
    return user


sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99,
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99,
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99,
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99,
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99,
}

sample_products = [
    Product(**sample_product_1),
    Product(**sample_product_2),
    Product(**sample_product_3),
    Product(**sample_product_4),
    Product(**sample_product_5),
]


@app.get("/product/search", response_model=list[Product])
async def search_product(keyword: str, category: str = None, limit: int = 10):
    if category:
        return list(
            prod for prod in sample_products if keyword.lower() in prod.name.lower() and prod.category == category
        )[:limit]
    else:
        return list(prod for prod in sample_products if keyword.lower() in prod.name.lower())[:limit]


@app.get("/product/{product_id}")
async def get_product_by_id(product_id: int):
    for prod in sample_products:
        if product_id == prod.product_id:
            return prod
    return {"error": f"no product with an id {product_id}"}


def write_log(email: str, message: str = ""):
    path = "logs.txt"
    with open(path, "a") as logs:
        logs.write(f"msg {message} sent to {email}")
        logs.write("\n")


@app.post("/send-notification/{email}")
async def send(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, email, message="notification")
    return {"msg": "background task added"}


@app.get("/items/")
async def read_items(ads_id: str | None = Cookie(default=None)):
    return {"ads_id": ads_id}


@app.get("/set_cookie")
async def set_cookie(response: Response):
    response.set_cookie(key="last_visit", value=f"{datetime.now()}")
    return {"msg": "куки доставлены"}


@app.get("/cookie")
async def get_cookie(last_visit=Cookie(default=None)):
    return {"last_visit": last_visit}


db_users = {"user123": "password123", "admin": "admin"}

session_store = {}


@app.post("/login", response_model=CommonMsg)
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    if username in db_users and db_users[username] == password:
        session_token = str(uuid.uuid4())
        session_store[session_token] = username
        response.set_cookie(key="session_token", value=session_token, secure=True, httponly=True)
        return {"msg": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/user")
async def check_user(session_token=Cookie(default=None)):
    if session_token is not None and session_token in session_store:
        username = session_store[session_token]
        return {"username": username, "profile_info": f"Welcome back, {username}!"}
    raise HTTPException(status_code=401, detail="Unauthorized")
