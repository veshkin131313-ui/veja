import requests


def convert(amount, from_currency, to_currency):
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
    response = requests.get(url)
    data = response.json()
    return data["rates"][to_currency]


print("Конвертер валют")
while True:
    try:
        amount = float(input("Введите сумму: "))
        break
    except ValueError:
        print("Нужно ввести число!")
from_cur = input("Из какой валюты (например, USD): ").upper()
to_cur = input("В какую валюту (например, EUR): ").upper()

result = convert(amount, from_cur, to_cur)
decimals = int(input("Сколько знаков после запятой выводить? "))
print(f"{amount} {from_cur} = {result:.{decimals}f} {to_cur}")
