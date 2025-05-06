from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from redis import asyncio as aioredis
from routes import router as router_auth


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        redis_connection = aioredis.from_url("redis://localhost:6379", encoding="utf8")
        await FastAPILimiter.init(redis_connection)
        print("redis connection open")
    except Exception as e:
        print(e)
    yield
    await FastAPILimiter.close()


app = FastAPI(lifespan=lifespan)


@app.get("/debug")
async def debug():
    print("DEBUG HIT")
    return {"ok": True}


app.include_router(router_auth)
# uvicorn auth.main:app --reload
