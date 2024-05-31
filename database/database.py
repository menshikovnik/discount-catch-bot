import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# db connect
conn = psycopg2.connect(
    dbname="bot_db",
    user="postgres",
    password=os.getenv("POSTGRES_PASSWORD"),
    host="localhost",
    port="5432"
)


def add_product(username, article, price, url, name_of_product):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO user_products (username, article, price, url, name_of_product) VALUES (%s, %s, %s, "
                    "%s, %s)",
                    (username, article, price, url, name_of_product))
        conn.commit()


def get_all_products(username):
    with conn.cursor() as cur:
        cur.execute("SELECT article, price, name_of_product, url FROM user_products WHERE username=%s", (username,))
        return cur.fetchall()


def close_connection():
    if conn:
        conn.close()
