
import httpx
import asyncio

from data.database import add_price

BITCOIN_PRICE_URL = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD"

# Получаем цену битка
async def fetch_bitcoin_price():
    async with httpx.AsyncClient() as client:
        response = await client.get(BITCOIN_PRICE_URL)
        data = response.json()
        return data["USD"]

# Цена битка + добавление в бд
async def update_bitcoin_price():
    while True:
        price = await fetch_bitcoin_price()
        await add_price(price=price)
        await asyncio.sleep(60)


# if __name__ == '__main__':
#     asyncio.run(update_bitcoin_price())