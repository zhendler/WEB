import aiohttp


class PrivatBankAPIClient:
    BASE_URL = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='

    async def fetch(self, date):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.BASE_URL}{date}") as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch data for {date}")
                return await response.json()
