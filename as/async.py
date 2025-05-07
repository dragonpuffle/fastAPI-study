import asyncio
import time

from fastapi import BackgroundTasks, FastAPI


app = FastAPI()


def sync_task():
    print("sync task")
    time.sleep(3)
    print("send email")


async def async_task():
    print("async task")
    await asyncio.sleep(3)
    print("done request to foreign api")


@app.post("/")
async def some_route(bg_tasks: BackgroundTasks):
    ...
    # asyncio.create_task(async_task())
    bg_tasks.add_task(sync_task)
    return {"ok": True}
