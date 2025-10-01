
import asyncio
import aiohttp
from history import save_record, load_history

# Функция конвертации
async def convert_async(session, amount, from_currency, to_currency):
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
    async with session.get(url) as response:
        data = await response.json()
        return data["rates"][to_currency]

# Получаем список валют
async def get_currencies_async(session):
    url = "https://api.frankfurter.app/currencies"
    async with session.get(url) as response:
        data = await response.json()
        return sorted(list(data.keys()))

# Функция безопасного ввода валюты
def input_currency(prompt, currencies, forbidden=None):
    while True:
        cur = input(prompt).strip().upper()
        if cur.lower() == "exit":
            print("Выход из программы...")
            exit()
        if len(cur) != 3:
            print("Код валюты должен состоять из 3 букв")
            continue
        if cur not in currencies:
            print("Такой валюты нет, нужно выбрать другую")
            continue
        if forbidden and cur == forbidden:
            print("Нельзя выбрать ту же валюту")
            continue
        return cur


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
                        print("2 — Показать историю по конкретной валюте")
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
                                print("4 - Назад в меню: ")
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