from app.api import convert_async
from app.history import save_record

async def convert_amount(session, amount: float, from_cur: str, to_currencies: list[str], decimals: int = 2) -> dict:
    """Конвертация суммы из одной валюты в несколько с сохранением в историю"""
    results = {}
    for to_cur in to_currencies:
        value = await convert_async(session, amount, from_cur, to_cur)
        formatted = f"{value:.{decimals}f}".rstrip("0").rstrip(".")
        results[to_cur] = formatted
        save_record(amount, from_cur, to_cur, formatted, decimals, clear=False)
    return results
