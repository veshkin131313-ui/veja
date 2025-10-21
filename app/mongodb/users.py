from app.schemas import User
from fastapi import HTTPException


async def create_user(username: str, password: str):
    exisitng = await User.find_one(User.username == username)
    if exisitng:
        raise HTTPException(status_code=409, detail="Пользователь уже зарегистрирован")
    user = User(username=username, password=password)
    await user.insert()
    return {"msg": f"Пользователь {username} зарегестрирован"}