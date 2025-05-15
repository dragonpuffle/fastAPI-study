import asyncpg
from motor.motor_asyncio import AsyncIOMotorDatabase

from real_db_app.database import get_db_connection_sqlite
from real_db_app.schemas import ItemSchema


async def create_item_pg(item: ItemSchema, db: asyncpg.Connection):
    query = """
    INSERT INTO items(name) VALUES($1)"""
    await db.execute(query, item.name)
    return {"message": "item created"}


def create_item_sqlite(item: ItemSchema):
    with get_db_connection_sqlite() as conn:
        cursor = conn.cursor()

        cursor.execute("INSERT INTO items(name) VALUES(?)", (item.name,))
        conn.commit()
    return {"message": "item created"}


async def create_item_mongo(item: ItemSchema, db: AsyncIOMotorDatabase):
    result = await db.items.insert_one(item.dict())
    return {"id": str(result.inserted_id)}
