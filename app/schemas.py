from pydantic import BaseModel, Field
from typing import List
from beanie import Document

class ConvertRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Сумма для конвертации")
    from_currency: str = Field(..., min_length=3, max_length=3, description="Валюта отправки")
    to_currencies: List[str] = Field(..., description="Список валют для конвертации")
    decimals: int = Field(2, ge=1, le=10, description="Количество знаков после запятой (1-10)")

class AuthData(BaseModel):
    username: str
    password: str

class User(Document):
    username: str
    password: str

    class Settings:
        name = "users"