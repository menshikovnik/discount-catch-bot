import asyncio
from catch_bot.bot import bot
from database.database import get_all_products_to_monitor, get_chat_id, update_product_price
from scripts.price_parser import Product


async def check_product(product):
    db_id, username, article, db_price = product

    product_info = await Product.fetch_product_details(article)

    if product_info.price < db_price:
        await update_product_price(article, product_info.price)
        await send_telegram_message(username, product_info)


async def check_database():
    products = await get_all_products_to_monitor()

    tasks = []
    for product in products:
        tasks.append(asyncio.create_task(check_product(product)))

    await asyncio.gather(*tasks)


async def send_telegram_message(user_id, product):
    chat_id = await get_chat_id(user_id)

    if chat_id:
        message = (f"Пользователь: {user_id}\n"
                   f"Товар: {product.name}\n"
                   f"Цена: {product.price}\n"
                   f"Ссылка: {product.url}")
        await bot.send_message(chat_id=chat_id, text=message)
    else:
        print(f"Chat ID для пользователя {user_id} не найден.")


async def start_price_monitor():
    while True:
        try:
            await check_database()
        except Exception as e:
            print(f"Ошибка при проверке базы данных: {e}")
            pass
        await asyncio.sleep(300)


async def start_price_monitor():
    while True:
        try:
            await check_database()
        except Exception as e:
            print(f"Ошибка при проверке базы данных: {e}")
            pass
        await asyncio.sleep(300)
