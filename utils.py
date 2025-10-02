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

def pluralize_decimals(n: int) -> str:
    if 11 <= n % 100 <= 14:
        return "знаков"
    elif n % 10 == 1:
        return "знак"
    elif 2 <= n % 10 <= 4:
        return "знака"
    else:
        return "знаков"