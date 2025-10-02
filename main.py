
import asyncio
import aiohttp
from api import convert_async, get_currencies_async
from utils import input_currency, pluralize_decimals
from history import save_record, load_history


async def main():
    async with aiohttp.ClientSession() as session:
        currencies = await get_currencies_async(session)

        #Главное меню
        while True:
            print("\nГлавное меню:")
            print("1 — Конвертация")
            print("2 — История")
            print("3 — Выход")
            choice = input("Выберите пункт: ").strip()

            if choice == "1":
                # --- Конвертация ---
                print("\nНовая конвертация")

                # Красивый вывод валют по 5 в строке
                print("Доступные валюты:")
                for i in range(0, len(currencies), 5):
                    print(" | ".join(currencies[i:i + 5]))

                # Ввод суммы
                while True:
                    user_input = input("Сумма (exit — выход): ").strip()
                    if user_input.lower() == "exit":
                        print("Выход из программы...")
                        exit()
                    try:
                        amount = float(user_input)
                        if amount <= 0:
                            print("Сумма должна быть больше нуля")
                            continue
                        break
                    except ValueError:
                        print("Нужно ввести число!")

                from_cur = input_currency("Валюта отправки (exit): ", currencies)

                while True:
                    to_input = input("В какие валюты конвертировать (через запятую, exit — выход): ").strip()
                    if to_input.lower() == "exit":
                        print("Выход из программы...")
                        exit()

                    to_currencies = [cur.strip().upper() for cur in to_input.replace(",", " ").split()]
                    invalid = [cur for cur in to_currencies if cur not in currencies or cur == from_cur]
                    if invalid:
                        print(f"Некорректные валюты: {', '.join(invalid)}. Попробуйте снова.")

                        continue
                    break


                # Выбор кол-ва знаков после запятой
                while True:
                    try:
                        decimals = int(input("Сколько знаков после запятой выводить? (от 1 до 10): "))
                        if decimals < 1 or decimals > 10:
                            print("Необходимо ввести число от 1 до 10")
                            continue
                        break
                    except ValueError:
                        print("Необходимо ввести целое число")

                results = {}
                for to_cur in to_currencies:
                    result = await convert_async(session, amount, from_cur, to_cur)
                    results[to_cur] = result

                for to_cur, value in results.items():
                    formatted = f"{value:.{decimals}f}".rstrip("0").rstrip(".")
                    print(f"{amount} {from_cur} = {formatted} {to_cur}")
                    # Сохраняем каждую конвертацию в историю
                    save_record(amount, from_cur, to_cur, formatted, decimals, clear=False)

            elif choice == "2":
                # --- Просмотр истории ---
                history = load_history()
                if not history:
                    print("\nИстория пуста")
                else:
                    while True:
                        print("\nИстория:")
                        print("1 — Вся история")
                        print("2 — Сортировка истории")
                        print("3 — Очистить историю")
                        print("4 — Назад в меню")
                        sub_choice = input("Выберите пункт: ").strip()
                        if sub_choice == "1":
                            for rec in history:
                                print(f"{rec['timestamp']} — {rec['amount']} {rec['from']} → {rec['to']} = {rec['result']} ({rec['decimals']} знака)")


                        elif sub_choice == "2":
                            while True:
                                print("1 - По валюте отправки: ")
                                print("2 - По валюте получения: ")
                                print("3 - По обеим валютам (отправки и получения): ")
                                print("4 - По дате и сумме: ")
                                print("5 - Назад в меню: ")
                                subb_choice = input("Выберите пункт: ").strip()
                                if subb_choice == "1":
                                    cur = input("Введите валюту отправки: ").strip().upper()
                                    filtered = [rec for rec in history if rec['from'] == cur]
                                    if not filtered:
                                        print("Нет записей с такой валютой.")
                                    else:
                                        for rec in filtered:
                                            print(
                                                f"{rec['timestamp']} — {rec['amount']} {rec['from']} → {rec['to']} = {rec['result']} ({rec['decimals']} знака)")

                                elif subb_choice == "2":
                                    cur = input("Введите валюту получения: ").strip().upper()
                                    filtered = [rec for rec in history if rec['to'] == cur]
                                    if not filtered:
                                        print("Нет записей с такой валютой.")
                                    else:
                                        for rec in filtered:
                                            print(
                                                f"{rec['timestamp']} — {rec['amount']} {rec['from']} → {rec['to']} = {rec['result']} ({rec['decimals']} знака)")

                                elif subb_choice == "3":

                                    from_cur = input("Введите валлюту отправки: ").strip().upper()
                                    to_cur = input("Введите валлюту получения: ").strip().upper()
                                    filtered = [rec for rec in history if
                                                rec['from'] == from_cur and rec["to"] == to_cur]
                                    if not filtered:
                                        print("Нет записей с такой парой валют.")
                                    else:
                                        for rec in filtered:
                                            print(
                                                f"{rec['timestamp']} — {rec['amount']} {rec['from']} → {rec['to']} = {rec['result']} ({rec['decimals']} знака)")

                                elif subb_choice == "4":
                                    while True:
                                        print("1 — По дате (старые → новые)")
                                        print("2 — По дате (новые → старые)")
                                        print("3 — По сумме (меньше → больше)")
                                        print("4 — По сумме (больше → меньше)")
                                        print("5 — Назад")

                                        sort_choice = input("Выберите пункт: ").strip()

                                        if sort_choice == "1":
                                            sorted_history = sorted(history, key=lambda x: x["timestamp"])
                                        elif sort_choice == "2":
                                            sorted_history = sorted(history, key=lambda x: x["timestamp"], reverse=True)
                                        elif sort_choice == "3":
                                            sorted_history = sorted(history, key=lambda x: float(x["amount"]))
                                        elif sort_choice == "4":
                                            sorted_history = sorted(history, key=lambda x: float(x["amount"]), reverse=True)
                                        elif sort_choice == "5":
                                            break
                                        else:
                                            print("Неверный пункт меню")
                                            continue

                                        for rec in sorted_history:
                                            print(f"{rec['timestamp']} — {rec['amount']} {rec['from']} → "
                                                  f"{rec['to']} = {rec['result']} ({rec['decimals']} {pluralize_decimals(rec['decimals'])})")
                                elif subb_choice == "5":
                                    break
                                else:
                                    print("Выбран неверный пункт меню")


                        elif sub_choice == "3":
                            while True:
                                cln_confirm = input("Вы уверены, что хотите удалить всю историю? (да/нет): ").strip().lower()
                                if cln_confirm == "да":
                                    save_record(None, None, None, None, None, clear=True)
                                    print("История успешно очищена!")
                                    break
                                elif cln_confirm == "нет":
                                    print("Очистка истории отменена.")
                                    break
                                else:
                                    print("Необходимо выбрать да/нет")


                        elif sub_choice == "4":
                             break
                        else:
                            print("Выбран неверный пункт меню")

            elif choice == "3":
                print("Выход из программы...")
                break

            else:
                print("Неверный пункт меню")

if __name__ == "__main__":
    asyncio.run(main())