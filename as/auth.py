from authx import AuthX, AuthXConfig
from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import BaseModel


app = FastAPI()

config = AuthXConfig()
config.JWT_SECRET_KEY = "LOL"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


class UserCredsSchema(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(creds: UserCredsSchema, response: Response):
    if creds.username == "admin" and creds.password == "admin_pass":
        user_id = 5
        token = security.create_access_token(uid=str(user_id))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")


@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():
    return {"message": "Welcome"}
