import asyncio
import websockets
import json
import aiohttp
from aiofile import AIOFile
from aiopath import AsyncPath
from datetime import datetime, timedelta

clients = {}
exchange_data = {}

API_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date={date}"

async def fetch_exchange_rates(date):
    url = API_URL.format(date=date.strftime('%d.%m.%Y'))
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def log_exchange_command():
    async with AIOFile("exchange.log", 'a') as afp:
        async with afp:
            await afp.write(f"{datetime.now()}: Exchange command executed\n")

async def update_exchange_data():
    global exchange_data
    today = datetime.now()
    exchange_data = {}
    for i in range(10):
        date = today - timedelta(days=i)
        data = await fetch_exchange_rates(date)
        exchange_data[date.strftime('%Y-%m-%d')] = {
            'EUR': next((item['rateBuy'] for item in data['exchangeRate'] if item['currency'] == 'EUR'), None),
            'USD': next((item['rateBuy'] for item in data['exchangeRate'] if item['currency'] == 'USD'), None)
        }

async def handle_exchange(params, websocket):
    await update_exchange_data()
    days = int(params[0]) if params else 0
    today = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    response = "Exchange rates:\n"
    for date, rates in exchange_data.items():
        if date >= start_date:
            response += f"{date}: EUR = {rates['EUR']}, USD = {rates['USD']}\n"
    
    await log_exchange_command()
    await websocket.send(response)

async def handler(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        action = data.get('action')
        
        if action == 'set_nickname':
            clients[websocket] = data['nickname']
            print(f"New client connected: {data['nickname']}")
        
        elif action == 'message':
            nickname = clients.get(websocket, 'Unknown')
            msg = f"{nickname}: {data['message']}"
            print(f"Broadcasting message: {msg}")
            # Broadcast the message to all connected clients
            for client in clients:
                if client != websocket:
                    await client.send(msg)
        
        elif action == 'exchange':
            params = data.get('params', [])
            await handle_exchange(params, websocket)

if __name__ == "__main__":
    start_server = websockets.serve(handler, "localhost", 5000)
    asyncio.get_event_loop().run_until_complete(start_server)
    print("WebSocket server started on ws://localhost:5000")
    asyncio.get_event_loop().run_forever()
