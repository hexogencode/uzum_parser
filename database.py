import sqlite3


def create_database():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    # Создание таблицы
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY,
                            title TEXT,
                            price INTEGER,
                            credit_price INTEGER
                          )''')
