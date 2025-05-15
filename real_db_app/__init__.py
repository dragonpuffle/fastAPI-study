import sys
import os

from fastapi import APIRouter

from real_db_app.routes import router

...
...

main_router = APIRouter()
main_router.include_router(router)
