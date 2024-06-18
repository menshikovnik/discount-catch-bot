import logging
import asyncio
from catch_bot.bot import bot
from aiogram import Dispatcher
from catch_bot.handlers import bot_menu
from scripts.check_price import start_price_monitor

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
dp.include_router(bot_menu.router)


async def setup_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def main():
    await asyncio.gather(
        setup_bot(),
        start_price_monitor()
    )


if __name__ == '__main__':
    asyncio.run(main())
