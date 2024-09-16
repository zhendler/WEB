import asyncio
import websockets

async def chat_client(uri: str, nickname: str):
    async with websockets.connect(uri) as websocket:
        print(f"Connected to {uri}")
        await websocket.send(f"/nick {nickname}")

        while True:
            message = input("You: ")
            if message.startswith("/exchange"):
                await websocket.send(message)
                response = await websocket.recv()
                print(f"Server: {response}")
            else:
                await websocket.send(message)
                response = await websocket.recv()
                print(f"Server: {response}")

if __name__ == "__main__":
    uri = input("Enter the WebSocket server URI (e.g., ws://localhost:5000): ")
    nickname = input("Enter your nickname: ")
    asyncio.run(chat_client(uri, nickname))
