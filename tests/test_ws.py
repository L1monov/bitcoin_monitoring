import websockets
import asyncio

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws/1"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello Server!")
        while True:
            response = await websocket.recv()
            print(response)

if __name__ == '__main__':
    asyncio.run(test_websocket())
