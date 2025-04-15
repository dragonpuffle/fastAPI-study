from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from auth.models import User


router = APIRouter()

engine = create_async_engine("sqlite+aiosqlite:///auth.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class AuthORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]


@router.post("/setup_db")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": "success"}


async def get_users(username: str, session: AsyncSession):
    query = select(AuthORM).where(AuthORM.username == username)
    result = await session.execute(query)
    return result.scalars().one_or_none()


async def add_users(data: User, session: AsyncSession):
    new_user = AuthORM(username=data.username, password=data.password)
    session.add(new_user)
    await session.commit()
    return {"ok": "success"}
