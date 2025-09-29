import json
import datetime
import os

HISTORY_FILE = "history.json"

# Сохранение новой записи
def save_record(amount, from_cur, to_cur, result, decimals):
    record = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "amount": amount,
        "from": from_cur,
        "to": to_cur,
        "result": result,
        "decimals": decimals
    }

    # Если файла нет — начинаем с пустого списка
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []

    # Добавляем запись
    history.append(record)

    # Перезаписываем файл
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)


# Загрузка истории
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []