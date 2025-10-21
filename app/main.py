# main.py
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from app.mongodb.mongo import init_db, close_db
from app.routers import convertation


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(lifespan=lifespan)

app.include_router(convertation.router)