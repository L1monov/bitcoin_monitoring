from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks, HTTPException
from pydantic import BaseModel
import httpx
import asyncio
import sqlite3
import time
from typing import Dict
from api_bitcoin.parsing_api import update_bitcoin_price
from notification_mail.check_price import check_price

from data import database

app = FastAPI()

# Кэш для хранения активных сессий
active_sessions: Dict[str, WebSocket] = {}


# WebSocket соединение для пользователей
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    active_sessions[user_id] = websocket
    # Тут ещё бы регу или чет тип такого чтобы email записывать
    await database.add_user(email=f'user_{user_id}@mail.ru', user_id=int(user_id))
    try:
        while True:
            price = await database.get_last_price()
            await websocket.send_text(f"Цена на биток: ${price[0]}")
            await asyncio.sleep(60)
    except WebSocketDisconnect:
        await database.update_status_user(user_id=int(user_id), status='inactive')
        del active_sessions[user_id]
        print(f"Пользователь {user_id} вышел")

@app.on_event("startup")
async def startup_event():
    # запускаем фоновую задачу на парсинг битка
    asyncio.create_task(update_bitcoin_price())

    # фоновую задачу на уведомление
    asyncio.create_task(check_price())
