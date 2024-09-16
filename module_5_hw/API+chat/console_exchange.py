import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta

class ExchangeRateFetcher:
    BASE_URL = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='

    async def fetch_rates(self, date):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.BASE_URL}{date}") as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch data for {date}")
                return await response.json()

    async def get_exchange_rates(self, days):
        tasks = [self.fetch_rates((datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y')) for i in range(days)]
        return await asyncio.gather(*tasks)

def main():
    if len(sys.argv) != 2:
        print("Usage: python console_exchange.py <days>")
        sys.exit(1)
    
    days = int(sys.argv[1])
    if days > 10:
        print("Error: You can only fetch exchange rates for the last 10 days.")
        sys.exit(1)
    
    fetcher = ExchangeRateFetcher()
    # Запуск асинхронної функції
    exchange_rates = asyncio.run(fetcher.get_exchange_rates(days))
    
    for rate in exchange_rates:
        print(rate)

if __name__ == "__main__":
    main()
