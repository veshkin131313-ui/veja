from operator import truediv
import requests

# Функция конвертации
def convert(amount, from_currency, to_currency):
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
    response = requests.get(url)
    data = response.json()
    return data["rates"][to_currency]

# Список доступных валют
def get_currencies():
    url = "https://api.frankfurter.app/currencies"
    try:
        response = requests.get(url)
        data = response.json()
        return list(data.keys())
    except Exception as e:
        raise RuntimeError(f"Ошибка епта: {e}")

# Функция ввода валюты
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

# Получаем список валют и сортируем
currencies = get_currencies()
currencies.sort()

# Красивый вывод валют по 5 в строке
print("Доступные валюты:")
for i in range(0, len(currencies), 5):
    print(" | ".join(currencies[i:i + 5]))

# Цикл повторного запуска конвертера
while True:
    print("\nНовая конвертация")

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

    # Вопрос о повторной конвертации
    again = input("Сделать еще одну конвертацию? (да/нет): ").strip().lower()
    if again != "да":
        print("Спасибо за использование конвертера!")
        break
