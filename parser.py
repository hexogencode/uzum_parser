import time
import sqlite3
from database import create_database
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def add_product(title, price, credit_price):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Добавление нового товара
    cursor.execute('''INSERT INTO products (title, price, credit_price) VALUES (?, ?, ?)''',
                   (title, price, credit_price))
    conn.commit()


def parse_products():
    time.sleep(10)

    product_elements = driver.find_elements(By.CLASS_NAME, 'subtitle-item')
    price_elements = driver.find_elements(By.CSS_SELECTOR, '.currency.product-card-price.slightly.medium')
    credit_elements = driver.find_elements(
        By.XPATH, "//div[@class='badge']//span[contains(@class, 'text') and contains(text(), 'сум/мес')]")

    for product_element, price_element, credit_element in zip(product_elements, price_elements, credit_elements):
        # Название
        title = product_element.text

        # Цена
        price_text = price_element.text
        price = int(price_text.replace(' ', '').replace('сум', ''))

        # Цена в рассрочку в месяц
        credit_text = credit_element.text
        credit = int(credit_text.replace(' ', '').replace('сум/мес', ''))

        add_product(title, price, credit)


def check_available():
    product_page = 1
    while True:
        # Переход на следующую страницу
        driver.get(link + '?currentPage=' + str(product_page))

        # Ожидание появления текста и если не находит - програма брейкается
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'subtitle-item')))
        if driver.find_elements(By.XPATH, "//div[@class='title' and text()='Мы не нашли подходящие товары']"):
            print("Товары не найдены. Программа завершена.")
            break
        else:
            parse_products()
            print(f'Товары с {product_page} страницы добавлены')
            print("Товары найдены. Продолжение работы программы.")
            product_page += 1


if __name__ == '__main__':
    link = input('Введите ссылку на страницу в узуме: ')
    driver = webdriver.Chrome()
    create_database()
    check_available()
