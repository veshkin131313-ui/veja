import requests

def convert(amount, from_currency, to_currency):
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
    response = requests.get(url)
    data = response.json()
    return data["rates"][to_currency]

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

#Цикл поторного запуска конвертера
while True:
    print("Новая конвертация")

#Вводим сумму
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


#Из какой валюты берем
    while True:
        from_cur = input("Валюта отправки (exit — выход):").strip().upper()
        if from_cur.lower() == "exit":
            print("Выход из программы...")
            exit()
        if len(from_cur) !=3:
            print("Код валюты должен состоять из 3 букв")
            continue
        if from_cur in currencies:
            break
        else:
            print("Такой валюты нет, нужно выбрать другую")


#В какую валюту
    while True:
        to_cur = input("Валюта получения (exit — выход):").strip().upper()
        if to_cur.lower() == "exit":
            print("Выход из программы...")
            exit()
        if len(to_cur) !=3:
            print("Код валюты должен состоять из 3 букв")
            continue
        if to_cur == from_cur:
            print("Нельзя выбрать ту же валюту")
            continue
        if to_cur in currencies:
            break
        else:
            print("Такой валюты нет, нужно выбрать другую")

#конвертация
    result = convert(amount, from_cur, to_cur)

#выбор кол-ва знаков после запятой
    while True:
        try:
            decimals = int(input("Сколько знаков после запятой выводить? (от 1 до 10) "))
            if decimals < 1 or decimals > 10:
                print("Необходимо ввести число от 1 до 10")
                continue
            break
        except ValueError:
            print("Необходимо ввести целое число")
    formatted_result = f"{result:.{decimals}f}".rstrip("0").rstrip(".")
    print(f"{amount} {from_cur} = {formatted_result} {to_cur}")

#вопрос о повторной конвертации
    again = input("Сделать еще одну конвертацию? (да/нет): ").strip().lower()
    if again != "да":
        print("Спасибо за использование конвертера!")
        break
