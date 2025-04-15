from fastapi import APIRouter, Depends, HTTPException

from auth.db import SessionDep, add_users, get_users
from auth.models import User
from auth.security import create_jwt_token, get_user_by_token, hash_password, verify_password


router = APIRouter()


@router.post("/login")
async def login(new_user: User, session: SessionDep):
    user = await get_users(new_user.username, session)
    if user is not None:
        if verify_password(new_user.password, user.password):
            token = create_jwt_token({"sub": new_user.username})
            return {"token": token, "token_type": "bearer"}
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/register")
async def register(new_user: User, session: SessionDep):
    existing_user = await get_users(new_user.username, session)
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")
    new_user.password = hash_password(new_user.password)
    result = await add_users(new_user, session)
    return {"result": result}


@router.get("/me", response_model=User)
async def get_me(session: SessionDep, current_user: str = Depends(get_user_by_token)):
    user = await get_users(current_user, session)
    if user:
        return User.model_validate(user)
    raise HTTPException(status_code=404, detail="User not found")
