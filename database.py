import sqlite3


def create_database():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Создание таблицы "Categories" с полями: id, name
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categories (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''')

    # Создание таблицы "Products" с полями: id, title, price, credit, category_id
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY,
            title TEXT,
            price INTEGER,
            credit INTEGER,
            link TEXT,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES Categories(id)
        )
    ''')

    conn.commit()
    conn.close()


def add_category(name):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Проверка наличия категории в базе данных
    cursor.execute('''
        SELECT id FROM Categories WHERE name = ?
    ''', (name,))
    category = cursor.fetchone()

    # Если категория не существует, вставляем новую категорию
    if not category:
        cursor.execute('''
            INSERT INTO Categories (name) VALUES (?)
        ''', (name,))
        conn.commit()
        category_id = cursor.lastrowid
    else:
        category_id = category[0]

    conn.close()
    return category_id


def check_existing_product(link):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Проверка наличия продукта с такой же ссылкой в базе данных
    cursor.execute('''
        SELECT id FROM Products WHERE link = ?
    ''', (link,))
    existing_product = cursor.fetchone()

    conn.close()

    return existing_product


def add_product(title, price, credit, link, category_name):
    # Проверяем, существует ли уже продукт с такой же ссылкой
    existing_product = check_existing_product(link)
    if existing_product:
        print("[-] Продукт уже существует в базе данных.")
        return

    # Если продукта с такой же ссылкой нет, добавляем новый продукт
    category_id = add_category(category_name)

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Вставка данных о продукте в таблицу
    cursor.execute('''
        INSERT INTO Products (title, price, credit, link, category_id) VALUES (?, ?, ?, ?, ?)
    ''', (title, price, credit, link, category_id))

    conn.commit()
    conn.close()
