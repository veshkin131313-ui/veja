# console_app.py
import asyncio
import aiohttp
from api import get_currencies_async
from utils import input_currency, input_amount, input_to_currencies
from converter import convert_amount
from history import load_history, show_history, clear_history

async def run_console():
    async with aiohttp.ClientSession() as session:
        currencies = await get_currencies_async(session)

        while True:
            print("\nГлавное меню:")
            print("1 — Конвертация")
            print("2 — История")
            print("3 — Выход")
            choice = input("Выберите пункт: ").strip()

            if choice == "1":
                print("Доступные валюты:")
                for i in range(0, len(currencies), 5):
                    print(" | ".join(currencies[i:i + 5]))

                amount = input_amount()
                if amount is None:
                    break

                from_cur = input_currency("Валюта отправки (exit): ", currencies)
                if from_cur is None:
                    break

                to_currencies = input_to_currencies(currencies=currencies, forbidden=from_cur)
                if to_currencies is None:
                    break

                while True:
                    try:
                        decimals = int(input("Сколько знаков после запятой выводить? (от 1 до 10): "))
                        if decimals < 1 or decimals > 10:
                            print("Необходимо ввести число от 1 до 10")
                            continue
                        break
                    except ValueError:
                        print("Необходимо ввести целое число")

                results = await convert_amount(session, amount, from_cur, to_currencies, decimals)
                for to_cur, value in results.items():
                    print(f"{amount} {from_cur} = {value} {to_cur}")

            elif choice == "2":
                history = load_history()
                show_history(history)

            elif choice == "3":
                print("Выход из программы...")
                break
            else:
                print("Неверный пункт меню")
