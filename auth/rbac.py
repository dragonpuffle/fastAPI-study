from dependencies import get_user_roles
from fastapi import Depends, HTTPException, Request, Response, Security
from fastapi.security import SecurityScopes
from fastapi_limiter.depends import RateLimiter


class PermissionChecker:
    def __init__(self, roles: list[str]):
        self.roles = roles

    def __call__(self, security_scopes: SecurityScopes, user_roles: list[str] = Security(get_user_roles)):
        print("вывод полученной роли", user_roles)
        if not user_roles:
            raise HTTPException(status_code=403, detail="Requires authentication")

        if "admin" in user_roles:
            return

        if not any(role in user_roles for role in self.roles):
            raise HTTPException(
                status_code=403,
                detail=f"Permission denied. Required: {security_scopes.scopes}",
                headers={"WWW-Authenticate": f"Bearer scope={security_scopes.scope_str}"},
            )


async def role_based_limit(
    request: Request, response: Response, user_roles: list[str] = Depends(get_user_roles)
) -> RateLimiter:
    if "admin" in user_roles:
        limiter = RateLimiter(times=1000, minutes=1)
    elif "user" in user_roles:
        limiter = RateLimiter(times=20, minutes=1)
    else:
        limiter = RateLimiter(times=3, minutes=1)
    return await limiter(request=request, response=response)
