from dependencies import get_user_roles
from fastapi import Depends, HTTPException


class PermissionChecker:
    def __init__(self, roles: list[str]):
        self.roles = roles

    def __call__(self, user_roles: list[str] = Depends(get_user_roles)):
        print("вывод полученной роли", user_roles)
        if not user_roles:
            raise HTTPException(status_code=403, detail="Requires authentication")

        if "admin" in user_roles:
            return

        if not any(role in user_roles for role in self.roles):
            raise HTTPException(status_code=403, detail="Permission denied")
