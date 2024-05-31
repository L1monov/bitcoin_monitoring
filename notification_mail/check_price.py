from data.database import get_last_price, get_inactive_email_user
from .send_mail import send_mail

import asyncio

async def check_price() -> None:
    prices = await get_last_price(limit=2)

    old_price, new_price = prices[0], prices[1]

    old_price = int(old_price)
    new_price = int(new_price)

    # првоерка прыгнула ли цена за 100 в любую сторону
    if str(old_price)[-3] != str(new_price)[-3]:
        email_inactive_users = await get_inactive_email_user()
        for email in email_inactive_users:
            await send_mail(email=email, price=new_price)

