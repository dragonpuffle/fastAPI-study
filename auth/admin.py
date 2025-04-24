import asyncio

from auth.db import setup_db


async def my_async_function():
    res = await setup_db()
    print(res)


if __name__ == "__main__":
    asyncio.run(my_async_function())
