from api_client import PrivatBankAPIClient
from datetime import datetime, timedelta
import asyncio

class ExchangeRateService:
    def __init__(self):
        self.client = PrivatBankAPIClient()

    async def get_rates(self, days):
        tasks = [self.client.fetch((datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y')) for i in range(days)]
        return await asyncio.gather(*tasks)
