import logging
import asyncio
from catch_bot.bot import bot
from aiogram import Dispatcher
from catch_bot.handlers import start_choose

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
dp.include_router(start_choose.router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
