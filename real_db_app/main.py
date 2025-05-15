from fastapi import FastAPI

from real_db_app import main_router


app = FastAPI()
app.include_router(main_router)
