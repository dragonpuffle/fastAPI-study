from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from models import Ideas, UserLogins, Users
from sqlalchemy import JSON, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


engine = create_async_engine("sqlite+aiosqlite:///auth.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class AuthORM(Base):
    __tablename__ = "user_logins"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    intro: Mapped[Optional[str]]
    roles: Mapped[list[str]] = mapped_column(JSON)


class IdeasORM(Base):
    __tablename__ = "ideas"

    id: Mapped[int] = mapped_column(primary_key=True)
    idea: Mapped[str]
    is_done: Mapped[bool]
    report: Mapped[Optional[str]]


async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": "success"}


async def get_user_logins_by_username(username: str, session: AsyncSession) -> UserLogins | None:
    query = select(AuthORM).where(AuthORM.username == username)
    result = await session.execute(query)
    return result.scalars().one_or_none()


async def get_users_by_username(username: str, session: AsyncSession) -> Users | None:
    query = select(UsersORM).where(UsersORM.username == username)
    result = await session.execute(query)
    return result.scalars().one_or_none()


async def add_user_logins(data: UserLogins, session: AsyncSession):
    is_exist = await get_user_logins_by_username(data.username, session)
    if is_exist:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = AuthORM(username=data.username, password=data.password)
    session.add(new_user)
    try:
        await session.commit()
        return {"ok": "success"}
    except IntegrityError:
        await session.rollback()
        raise


async def add_users(data: Users, session: AsyncSession):
    is_exist = await get_users_by_username(data.username, session)
    if is_exist:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = UsersORM(
        username=data.username, full_name=data.full_name, email=data.email, intro=data.intro, roles=data.roles
    )
    session.add(new_user)
    try:
        await session.commit()
        return {"ok": "success"}
    except IntegrityError:
        await session.rollback()
        raise


async def view_ideas(session: AsyncSession):
    query = select(IdeasORM)
    result = await session.execute(query)
    return result.scalars().all()


async def update_ideas(idea_id: int, data: Ideas, session: AsyncSession):
    query = select(IdeasORM).where(IdeasORM.id == idea_id)
    result = await session.execute(query)
    idea = result.scalars().first()

    if idea:
        idea.is_done = data.is_done
        idea.report = data.report

    try:
        await session.commit()
        return {"ok": "success"}
    except IntegrityError:
        await session.rollback()
        raise


async def add_ideas(data: Ideas, session: AsyncSession):
    new_idea = IdeasORM(idea=data.idea, is_done=data.is_done, report=data.report)
    session.add(new_idea)

    try:
        await session.commit()
        return {"ok": "success"}
    except IntegrityError:
        await session.rollback()
        raise
