import json
import datetime
import os
from utils import pluralize_decimals

HISTORY_FILE = "history.json"

def save_record(amount, from_cur, to_cur, result, decimals, clear=False):
    """Сохранение или очистка истории"""
    if clear:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            f.write("[]")
        return

    record = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "amount": amount,
        "from": from_cur,
        "to": to_cur,
        "result": result,
        "decimals": decimals
    }

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []

    history.append(record)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def load_history():
    """Загрузка истории"""
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def show_history(history: list[dict]):
    """Вывод всей истории"""
    if not history:
        print("История пуста")
        return
    for rec in history:
        print(f"{rec['timestamp']} — {rec['amount']} {rec['from']} → {rec['to']} = {rec['result']} ({rec['decimals']} {pluralize_decimals(rec['decimals'])})")

def clear_history():
    """Очистка истории"""
    save_record(None, None, None, None, None, clear=True)
