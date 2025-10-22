import asyncio
from contextlib import asynccontextmanager

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update

from configs import TOKEN, WEBHOOK_URL
from fastapi import FastAPI, Request
from handlers.start import router as start_router
from handlers.lead import router as lead_router

default_properties = DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
bot = Bot(TOKEN, default=default_properties)
dp = Dispatcher()


def include():
    dp.include_router(start_router)
    dp.include_router(lead_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    include()
    await bot.set_webhook(WEBHOOK_URL)
    print("Сервер Запущен")
    yield
    print("Работа Завершилась")
    await bot.delete_webhook()
    await bot.session.close()


app = FastAPI(
    lifespan=lifespan,
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/")
async def process_webhook(request: Request):
    data = await request.json()
    update = Update(**data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}

async def main():
    include()
    await dp.start_polling(bot)

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8001)
    asyncio.run(main())
