from pymongo import AsyncMongoClient
from beanie import init_beanie
from app.schemas import User

client: AsyncMongoClient | None = None
MONGO_URL="mongodb://localhost:27017"
async def init_db():
    global client
    client = AsyncMongoClient(MONGO_URL)
    await init_beanie(
        database = client["converter+"],
        document_models=[User],
    )

async def close_db():
    global client
    if client is not None:
        client.close()