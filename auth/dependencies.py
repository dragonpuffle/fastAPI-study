from db import SessionDep, get_users_by_username
from fastapi import Depends, HTTPException
from security import get_username_by_token


async def get_user_roles(session: SessionDep, username: str = Depends(get_username_by_token)) -> list[str]:
    user = await get_users_by_username(username, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.roles
