from http.cookiejar import request_path
from operator import truediv
import requests
from history import save_record, load_history

# Функция конвертации
def convert(amount, from_currency, to_currency):
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
    response = requests.get(url)
    data = response.json()
    return data["rates"][to_currency]

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

# Получаем список валют
def get_currencies():
    url = "https://api.frankfurter.app/currencies"
    try:
        response = requests.get(url)
        data = response.json()
        return sorted(list(data.keys()))
    except Exception as e:
        raise RuntimeError(f"Ошибка подключения: {e}")

currencies = get_currencies()

# Главное меню
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

        # Ввод валют
        from_cur = input_currency("Валюта отправки (exit): ", currencies)
        to_cur   = input_currency("Валюта получения (exit): ", currencies, forbidden=from_cur)

        # Конвертация
        result = convert(amount, from_cur, to_cur)

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

        formatted_result = f"{result:.{decimals}f}".rstrip("0").rstrip(".")
        print(f"{amount} {from_cur} = {formatted_result} {to_cur}")

        # Сохраняем запись в историю
        save_record(amount, from_cur, to_cur, formatted_result, decimals)

    elif choice == "2":
        # --- Просмотр истории ---
        history = load_history()
        if not history:
            print("\nИстория пуста")
        else:
            print("\nИстория конвертаций:")
            for rec in history:
                print(f"{rec['timestamp']} — {rec['amount']} {rec['from']} → {rec['to']} = {rec['result']} ({rec['decimals']} знака)")

    elif choice == "3":
        print("Выход из программы...")
        break

    else:
        print("Неверный пункт меню")
