class ExchangeRateFormatter:
    def format(self, rates):
        # Вибираємо тільки валюту "USD" та "EUR"
        filtered_rates = [
            {
                'date': rate['date'],
                'USD': next((r['saleRateNB'] for r in rate['exchangeRate'] if r['currency'] == 'USD'), 'N/A'),
                'EUR': next((r['saleRateNB'] for r in rate['exchangeRate'] if r['currency'] == 'EUR'), 'N/A')
            }
            for rate in rates
        ]

        # Форматування результату
        formatted_output = "Date       | USD Rate  | EUR Rate\n"
        formatted_output += "-" * 35 + "\n"

        for rate in filtered_rates:
            formatted_output += f"{rate['date']:<10} | {rate['USD']:<8} | {rate['EUR']:<8}\n"

        return formatted_output
