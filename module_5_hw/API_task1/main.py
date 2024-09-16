import sys
import asyncio
from exchange_rate_service import ExchangeRateService
from exchange_rate_formatter import ExchangeRateFormatter

async def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <days>")
        sys.exit(1)

    days = int(sys.argv[1])
    if days > 10:
        print("Error: You can only fetch exchange rates for the last 10 days.")
        sys.exit(1)

    service = ExchangeRateService()
    rates = await service.get_rates(days)
    formatter = ExchangeRateFormatter()



    formatted_rates = formatter.format(rates)
    print(formatted_rates)

if __name__ == "__main__":
    asyncio.run(main())
