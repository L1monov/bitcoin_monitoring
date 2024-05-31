import time

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.future import select
from databases import Database
from datetime import datetime
from pydantic import BaseModel
from config import DATABASE_URL
import asyncio

import logging



# подключение
database = Database(DATABASE_URL)
async_engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)



# схема
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, index=True)
    status = Column(String, default='active')

class Price(Base):
    __tablename__ = "price"
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

async def create_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_price(price: float) -> None:
    """
    Добавляем цену
    :param price: цена битка
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            new_price = Price(price=price)
            session.add(new_price)



async def add_user(user_id: int, email: str) -> None:
    """
    Добавляем нового пользователя
    :param email: mail user
    :return:
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Проверяем, существует ли пользователь с таким email
            result = await session.execute(
                select(User).where(User.email == email)
            )
            existing_user = result.scalar_one_or_none()
            if existing_user is not None:
                # если есть, значит он зашел и надо статус на активный поставить
                await update_status_user(user_id=user_id, status='active')
                return

            new_user = User(email=email)
            session.add(new_user)

async def update_status_user(user_id: int, status: str) -> None:
    """
    Обновляем статус пользователю, если отключился или подключился
    :param user_id:
    :param status:
    :return:
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()

            # Обновляем статус пользователя
            user.status = status
            session.add(user)

async def get_mail_user(user_id: int) -> str:
    """
    Получаем маил юзера
    :param user_id:
    :return:
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(
                select(User.email).where(User.id == user_id)
            )
            return result.scalar_one_or_none()

async def get_last_price(limit=1) -> float:
    """
    Получаем последнюю цену биткоина
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(
                select(Price.price).order_by(Price.timestamp.desc()).limit(limit)
            )
            last_prices = result.scalars().all()
            return last_prices

async def get_inactive_email_user() -> list:
    """
    Получаем всех не активных пользователей
    :return:
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(
                select(User.email).where(User.status == 'inactive')
            )

            return result.scalars().all()





#
# async def add_user(email):
#     query = User.__table__.insert().values( email=email)
#     await database.execute(query)
#
#
# async def get_user(user_id):
#     query = User.__table__.select().where(User.id == user_id)
#     return await database.fetch_one(query)
#
# async def add_price_alert(price):
#     await database.connect()
#     query = Price.__table__.insert().values(price=price)
#     await database.execute(query)
#
#     await database.disconnect()
#
#
# async def get_latest_price():
#     query = Price.__table__.select().order_by(Price.timestamp.desc()).limit(1)
#     row = await database.fetch_one(query)
#     return row.price if row else None
#
# async def get_price_history(limit=2):
#     query = Price.__table__.select().order_by(Price.timestamp.desc()).limit(limit)
#     rows = await database.fetch_all(query)
#     return [row.price for row in rows]
#
# async def get_all_users():
#     query = User.__table__.select()
#     return await database.fetch_all(query)





