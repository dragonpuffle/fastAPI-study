import sqlite3
from contextlib import asynccontextmanager

import asyncpg
from motor.motor_asyncio import AsyncIOMotorClient


DATABASE_URL_PG = "postgresql://fastapi_user:fastapi_pass@localhost:5432/fastapi"


@asynccontextmanager
async def get_db_connection_pg():
    conn = await asyncpg.connect(DATABASE_URL_PG)
    try:
        yield conn
    finally:
        await conn.close()


# DATABASE_URL_sqlite = "sqlite+aiosqlite:///database.db"
# engine_sqlite = create_async_engine(DATABASE_URL_sqlite)
# new_session = async_sessionmaker(engine_sqlite, expire_on_commit=False)
#
# @asynccontextmanager
# async def get_db_connection_sqlite():
#     async with new_session() as session:
#         yield session

DB_NAME_SQLITE = "database.sqlite"


def get_db_connection_sqlite():
    conn = sqlite3.connect(DB_NAME_SQLITE)
    conn.row_factory = sqlite3.Row
    return conn


DATABASE_URL_MONGO = "mongodb://localhost:27017"
DB_NAME_MONGO = "mydatabase"


async def get_db_connection_mongo():
    client = AsyncIOMotorClient(DATABASE_URL_MONGO)
    db = client[DB_NAME_MONGO]
    try:
        yield db
    finally:
        client.close()
