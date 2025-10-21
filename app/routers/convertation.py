from fastapi import FastAPI, HTTPException, APIRouter
import aiohttp
from app.converter import convert_amount
from app.api import get_currencies_async
from app.schemas import ConvertRequest
from app.history import load_history, clear_history
from fastapi import Query

router = APIRouter(prefix="/converter", tags=["converter"])\

@router.get("")
async def convert(
    amount: float = Query(..., gt=0, description="Сумма для конвертации"),
    from_currency: str = Query(..., min_length=3, max_length=3, description="Валюта отправки"),
    to_currencies: str = Query(..., description="Список валют через запятую (например: EUR,GBP)"),
    decimals: int = Query(2, ge=1, le=10, description="Количество знаков после запятой (1-10)")
):
    async with aiohttp.ClientSession() as session:
        currencies = await get_currencies_async(session)

        from_cur = from_currency.upper()
        to_list = [cur.strip().upper() for cur in to_currencies.split(",")]

        # Проверка валют
        if from_cur not in currencies:
            raise HTTPException(status_code=400, detail=f"Валюта отправки '{from_cur}' недоступна")
        invalid = [cur for cur in to_list if cur not in currencies or cur == from_cur]
        if invalid:
            raise HTTPException(status_code=400, detail=f"Некорректные валюты: {', '.join(invalid)}")

        # Конвертация
        results = await convert_amount(session, amount, from_cur, to_list, decimals)

        return {
            "amount": amount,
            "from_currency": from_cur,
            "results": results
        }

# --- История ---
@router.get("/history")
def get_history():
    history = load_history()
    return {"history": history}

# --- Очистка истории ---
@router.delete("/history")
def delete_history():
    clear_history()
    return {"message": "История очищена"}