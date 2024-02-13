import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from database import *


def parse_products(category):
    # Поиск элементов
    title_elements = driver.find_elements(By.CLASS_NAME, 'subtitle-item')
    price_elements = driver.find_elements(By.CSS_SELECTOR, '.currency.product-card-price.slightly.medium')
    credit_elements = driver.find_elements(
        By.XPATH, "//div[@class='badge']//span[contains(@class, 'text') and contains(text(), 'сум/мес')]")
    link_elements = driver.find_elements(By.CLASS_NAME, 'subtitle-item')

    for product_element, price_element, credit_element, link_element in zip(title_elements, price_elements,
                                                                            credit_elements, link_elements):
        # Название
        title = product_element.text

        # Цена
        price_text = price_element.text
        price = int(price_text.replace(' ', '').replace('сум', ''))

        # Цена в рассрочку в месяц
        credit_text = credit_element.text
        credit = int(credit_text.replace(' ', '').replace('сум/мес', ''))

        # Ссылка на товар
        link = link_element.get_attribute('href')

        # Добавление продукта в БД
        add_product(title, price, credit, link, category)


# При каждой итерации цикла проверяет есть ли что парсить
def check_availability(category):
    product_page = 1
    while True:
        # Переход на следующую страницу
        driver.get(link + '?currentPage=' + str(product_page))

        # Ожидание появления текста и если не находит - програма брейкается
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'subtitle-item')))
        if driver.find_elements(By.XPATH, "//div[@class='title' and text()='Мы не нашли подходящие товары']"):
            print("[!] Товары не найдены. Программа завершена.")
            break
        else:
            parse_products(category)
            print(f'[+] Продукты с {product_page} страницы успешно добавлены')
            product_page += 1


if __name__ == '__main__':
    link = input('Введите ссылку на страницу в Uzum: ')

    # Что бы не открывался браузер, он открывается в режиме headless (код можно удалить для визуала)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x935')
    driver = webdriver.Chrome(options=options)

    # Создать базу данных если еще не создана
    create_database()
    # Добавить категорию без
    add_category(link)
    # Проверять если продукты кончаться - брейк
    check_availability(link)
