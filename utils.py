def input_currency(prompt, currencies, forbidden=None):
    """Безопасный ввод валюты"""
    while True:
        cur = input(prompt).strip().upper()
        if cur.lower() == "exit":
            return None
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

def pluralize_decimals(n: int) -> str:
    if 11 <= n % 100 <= 14:
        return "знаков"
    elif n % 10 == 1:
        return "знак"
    elif 2 <= n % 10 <= 4:
        return "знака"
    else:
        return "знаков"

def input_amount(prompt="Сумма (exit — выход): "):
    """Безопасный ввод суммы"""
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == "exit":
            return None
        try:
            amount = float(user_input)
            if amount <= 0:
                print("Сумма должна быть больше нуля")
                continue
            return amount
        except ValueError:
            print("Нужно ввести число!")

def input_to_currencies(prompt="В какие валюты конвертировать (через запятую, exit — выход): ", currencies=None, forbidden=None):
    """Ввод списка валют для конвертации"""
    while True:
        to_input = input(prompt).strip()
        if to_input.lower() == "exit":
            return None
        to_currencies = [cur.strip().upper() for cur in to_input.replace(",", " ").split()]
        invalid = [cur for cur in to_currencies if cur not in currencies or cur == forbidden]
        if invalid:
            print(f"Некорректные валюты: {', '.join(invalid)}. Попробуйте снова.")
            continue
        return to_currencies
