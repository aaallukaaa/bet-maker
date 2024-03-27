from fastapi import FastAPI

from src.config import config
from src.router import router as bet_router


app = FastAPI(title=config.APP_NAME)

app.include_router(bet_router)
