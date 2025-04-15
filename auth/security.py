import datetime
import time
from typing import Dict

import jwt
from environs import Env
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
env = Env()
env.read_env()


def create_jwt_token(data: Dict):
    to_encode = data.copy()
    expires = datetime.datetime.fromtimestamp(time.time()) + datetime.timedelta(minutes=env.ACCESS_TOKEN_EXPIRY)
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, env.SECRET_KEY_AUTH, algorithm=env.ALGORITHM)


def get_user_by_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, env.SECRET_KEY_AUTH, algorithms=[env.ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        pass
    except jwt.InvalidTokenError:
        pass


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
