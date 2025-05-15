import asyncio

from real_db_app.database import get_db_connection_pg, get_db_connection_sqlite


async def create_table_pg():
    async with get_db_connection_pg() as conn:
        query = """CREATE TABLE IF NOT EXISTS items
        (id SERIAL PRIMARY KEY,
        NAME TEXT NOT NULL)"""
        await conn.execute(query)


def create_table_sqlite():
    with get_db_connection_sqlite() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
        )
        conn.commit()


if __name__ == "__main__":
    asyncio.run(create_table_pg())
    create_table_sqlite()
