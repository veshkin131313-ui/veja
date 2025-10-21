# main.py
import uvicorn
from app import app  # твой файл app.py с FastAPI эндпоинтами

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
