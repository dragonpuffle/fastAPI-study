from fastapi import APIRouter, Depends

from real_db_app.crud import create_item_mongo, create_item_pg, create_item_sqlite
from real_db_app.database import get_db_connection_mongo, get_db_connection_pg
from real_db_app.schemas import ItemSchema


router = APIRouter()


@router.post("/items", status_code=201)
async def create_item_route(item: ItemSchema, db=Depends(get_db_connection_pg)):
    result = await create_item_pg(item, db)
    return result


@router.post("/items_sqlite", status_code=201)
def create_item_route_sqlite(item: ItemSchema):
    result = create_item_sqlite(item)
    return result


@router.post("/items_mongo", status_code=201)
async def create_item_route_mongo(item: ItemSchema, db=Depends(get_db_connection_mongo)):
    result = await create_item_mongo(item, db)
    return result
