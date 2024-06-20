import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONFIG = {
    'user': 'postgres',
    'password': 'test',
    'database': 'bot_db',
    'host': 'postgres',
    'port': '5432'
}


async def create_connection():
    return await asyncpg.connect(**DATABASE_CONFIG)


async def add_product(username, article, price, url, name_of_product):
    conn = await create_connection()
    async with conn.transaction():
        await conn.execute(
            "INSERT INTO user_products (username, article, price, url, name_of_product) VALUES ($1, $2, $3, $4, $5)",
            username, article, price, url, name_of_product
        )
    await conn.close()


async def get_all_products(username):
    conn = await create_connection()
    try:
        result = await conn.fetch(
            "SELECT article, price, name_of_product, url FROM user_products WHERE username=$1",
            username
        )
        return result
    finally:
        await conn.close()


async def save_chat_id(user_id, chat_id, username):
    conn = await create_connection()
    async with conn.transaction():
        exists = await conn.fetchval(
            "SELECT 1 FROM users WHERE user_id=$1",
            user_id
        )
        if exists:
            await conn.execute(
                "UPDATE users SET chat_id=$1, username=$2 WHERE user_id=$3",
                chat_id, username, user_id
            )
        else:
            await conn.execute(
                "INSERT INTO users (user_id, chat_id, username) VALUES ($1, $2, $3)",
                user_id, chat_id, username
            )
    await conn.close()


async def get_chat_id(username):
    conn = await create_connection()
    try:
        result = await conn.fetchval(
            "SELECT chat_id FROM users WHERE username=$1",
            username
        )
        return result
    finally:
        await conn.close()


async def get_all_products_to_monitor():
    conn = await create_connection()
    try:
        result = await conn.fetch(
            "SELECT id, username, article, price, url FROM user_products"
        )
        return result
    finally:
        await conn.close()


async def update_product_price(product_id, new_price):
    conn = await create_connection()
    try:
        async with conn.transaction():
            await conn.execute(
                "UPDATE user_products SET price = $1 WHERE article = $2",
                new_price, product_id
            )
    except Exception as e:
        print(f"Error updating product price: {e}")
    finally:
        await conn.close()


async def delete_product(product_art, username):
    conn = await create_connection()
    try:
        async with conn.transaction():
            await conn.execute(
                "DELETE FROM user_products WHERE article = $1 AND username = $2",
                product_art, username
            )
    except Exception as e:
        print(f"Error deleting product: {e}")
    finally:
        await conn.close()


async def get_name_of_product(product_art, username):
    conn = await create_connection()
    try:
        async with conn.transaction():
            result = await conn.fetchval(
                "SELECT name_of_product FROM user_products WHERE article = $1 AND username = $2",
                product_art, username
            )
            return result
    except Exception as e:
        print(f"Error getting name_of_product: {e}")
    finally:
        await conn.close()


async def close_connection(conn):
    await conn.close()
