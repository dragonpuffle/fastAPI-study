from functools import wraps

from fastapi import HTTPException


class PermissionChecker:
    def __init__(self, roles: list[str]):
        self.roles = roles

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_roles = kwargs.get("user_roles")
            print(user_roles)
            if not user_roles:
                raise HTTPException(status_code=403, detail="Requires authentication")

            if "admin" in user_roles:
                return await func(*args, **kwargs)

            if not any(role in user_roles for role in self.roles):
                raise HTTPException(status_code=403, detail="Permission denied")
            return await func(*args, **kwargs)

        return wrapper
