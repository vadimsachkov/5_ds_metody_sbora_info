from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from pprint import pprint
from pymongo import MongoClient
import time


def get_mvideo_sale_hits(to_mongo=False):
    browser_options = Options()
    browser_options.add_argument('start-maximized')

    driver = webdriver.Chrome('./chromedriver', options=browser_options)

    try:
        driver.get('https://www.mvideo.ru/')
    except WebDriverException:
        print('\n\tОшибка! Не удается соединиться с "mvideo.ru"!')
        return 0, driver

    # Проверяю загрузились ли "Хиты продаж" по наличию на странице следующего за ним блока
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"h2")][contains(text(),"Новинки")]')))
    except TimeoutException:
        print(f'\n\t\tОшибка: не удалось загрузить страницу!')
        return 0, driver

    if to_mongo:
        client = MongoClient('127.0.0.1', 27017)
        db = client['db_mvideo_ru']
        mongo = db.hits

    # Контроль расположения на странице блока "Хиты продаж"
    h2_list = driver.find_elements_by_xpath('//div[contains(@class,"h2")]')
    hits_index = None
    for i in range(len(h2_list)):
        if 'Хиты' in h2_list[i].text:
            hits_index = i
            break

    if hits_index == None:
        print(f'\n\t\tОшибка: блок "Хиты продаж" не найден на странице!')
        return 0, driver

    carousel_list = driver.find_elements_by_xpath('//ul[contains(@data-init,"galleryCarousel")]')

    print('\n"Хиты продаж:"')

    while True:
        product_card_list = carousel_list[hits_index].find_elements_by_xpath('./li/div')

        for i in range(4):
            product_data_dict = {}

            product_data_dict['name'] = product_card_list[i].find_element_by_xpath('.//h4').get_attribute('title')
            product_data_dict['price'] = product_card_list[i].find_element_by_xpath(
                './/div[contains(@data-sel,"div-price_current")]').text.replace(' ', '')[:-1]

            pprint(product_data_dict)

            if to_mongo:
                mongo.insert_one(product_data_dict)

        next = carousel_list[hits_index].find_element_by_xpath('./../../a[contains(@class,"next-btn")]')

        if 'disabled' in next.get_attribute('class'):
            break

        next.click()
        time.sleep(3)

    if to_mongo:
        return mongo.count_documents({}), driver
    else:
        return 'Запись в БД не производилась!', driver


print('\n============= Домашняя работа 5 - задание 2 =============')
print('=========================================================\n')

to_mongo = None
while not to_mongo:
    to_mongo = input('Сохранять данные о товарах в БД? (y/n): ').strip().lower()
    if to_mongo in ['y', 'yes']:
        to_mongo = True
        break
    elif to_mongo in ['n', 'no']:
        to_mongo = False
        break
    else:
        to_mongo = None

result = get_mvideo_sale_hits(to_mongo=to_mongo)

print('\nРезультат:')
print(f'\tДобавлено товаров в БД: {result[0]}')

input('\n\nНажмите любую клавишу для закрытия браузера и завершения работы...')
result[1].quit()