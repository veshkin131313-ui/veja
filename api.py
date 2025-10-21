import aiohttp
# Асинхронная конвертация валют
async def convert_async(session, amount, from_currency, to_currency):
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
    async with session.get(url) as response:
        data = await response.json()
        return data["rates"][to_currency]

# Получение списка валют
async def get_currencies_async(session):
    url = "https://api.frankfurter.app/currencies"
    async with session.get(url) as response:
        data = await response.json()
        return sorted(list(data.keys()))