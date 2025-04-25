import datetime
from typing import Dict

import jwt
from db import SessionDep, get_user_logins_by_username
from environs import Env
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
env = Env()
env.read_env()


def create_jwt_token(data: Dict):
    to_encode = data.copy()
    expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=env.int("ACCESS_TOKEN_EXPIRE_MINUTE"))
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, env("SECRET_KEY_AUTH"), algorithm=env("ALGORITHM"))


async def get_username_by_token(session: SessionDep, token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, env("SECRET_KEY_AUTH"), algorithms=[env("ALGORITHM")])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        user = await get_user_logins_by_username(username, session)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return user.username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
