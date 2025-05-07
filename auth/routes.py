from db import (
    SessionDep,
    add_ideas,
    add_user_logins,
    add_users,
    get_user_logins_by_username,
    get_users_by_username,
    update_ideas,
    view_ideas,
)
from dependencies import get_user_roles
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.openapi.models import Response
from models import Ideas, UserLogins, Users
from rbac import PermissionChecker, role_based_limit
from security import create_jwt_token, get_username_by_token, hash_password, verify_password


router = APIRouter()


@router.post("/login")
async def login(new_user: UserLogins, session: SessionDep, response: Response):
    user = await get_user_logins_by_username(new_user.username, session)
    if user and verify_password(new_user.password, user.password):
        token = create_jwt_token({"sub": new_user.username})
        # response.set_cookie(key='token', values=token)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/register")
async def register(new_user: UserLogins, session: SessionDep):
    existing_user = await get_user_logins_by_username(new_user.username, session)
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")
    new_user.password = hash_password(new_user.password)
    try:
        result = await add_user_logins(new_user, session)
        return {"result": result}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to create user")


@router.get("/me", response_model=Users)
async def get_me(session: SessionDep, current_user: str = Depends(get_username_by_token)):
    user = await get_users_by_username(current_user, session)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/me")
async def add_me(session: SessionDep, user_data: Users, current_user: str = Depends(get_username_by_token)):
    user = await add_users(user_data, session)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@router.get("/ideas", response_model=list[Ideas], dependencies=[Depends(role_based_limit)])
async def get_ideas(
    session: SessionDep,
    user_roles: list[str] = Depends(get_user_roles),
    permission: None = Security(PermissionChecker(["guest", "user"])),
):
    ideas = await view_ideas(session)
    if ideas:
        return ideas
    raise HTTPException(status_code=404, detail="No ideas found")


@router.post("/ideas")
async def add_ideas_route(
    session: SessionDep,
    idea: Ideas,
    user_roles: list[str] = Depends(get_user_roles),
    permission: None = Security(PermissionChecker(["admin"])),
):
    result = await add_ideas(idea, session)
    return result


@router.put("/ideas/{idea_id}")
async def update_ideas_route(
    session: SessionDep,
    idea_id: int,
    idea: Ideas,
    user_roles: list[str] = Depends(get_user_roles),
    permission: None = Security(PermissionChecker(["user"])),
):
    result = await update_ideas(idea_id, idea, session)
    return result
