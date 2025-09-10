import requests


def convert(amount, from_currency, to_currency):
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
    response = requests.get(url)
    data = response.json()
    return data["rates"][to_currency]


#Вводим сумму
print("Конвертер валют")
while True:
    try:
        amount = float(input("Введите сумму: "))
        break
    except ValueError:
        print("Нужно ввести число!")


#список доступных валют
def get_currencies():
    url= "https://api.frankfurter.app/currencies"
    try:
        response = requests.get(url)
        data = response.json()
        return list(data.keys())
    except Exception as e:
        raise RuntimeError(f"Ошибка епта: {e}")
currencies = get_currencies()
print("Доступные валюты:", " | ".join(currencies))


#Из какой валюты берем
while True:
    from_cur = input(f"Из какой валюты:").upper()
    if len(from_cur) !=3:
        print("Код валюты должен состоять из 3 букв")
        continue
    if from_cur in currencies:
        break
    else:
        print("Такой валюты нет, нужно выбрать другую")


#В какую валюту
while True:
    to_cur = input(f"В какую валюту:").upper()
    if len(to_cur) !=3:
        print("Код валюты должен состоять из 3 букв")
        continue
    if to_cur in currencies:
        break
    else:
        print("Такой валюты нет, нужно выбрать другую")


result = convert(amount, from_cur, to_cur)
decimals = int(input("Сколько знаков после запятой выводить? "))
formatted_result = f"{result:.{decimals}f}".rstrip("0").rstrip(".")
print(f"{amount} {from_cur} = {formatted_result} {to_cur}")