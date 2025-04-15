from fastapi import FastAPI

from auth.db import router as router_db
from auth.routes import router as router_auth


app = FastAPI()
app.include_router(router_db)
app.include_router(router_auth)
# some problems
