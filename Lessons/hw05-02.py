# pip install selenium

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from pymongo import MongoClient
from pprint import pprint
import json

'''2. Написать программу, которая собирает «Хиты продаж» с сайтов техники М.видео, ОНЛАЙН
ТРЕЙД и складывает данные в БД. Магазины можно выбрать свои. Главный критерий выбора:
динамически загружаемые товары.
'''

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome('./chromedriver.exe', options=chrome_options)

driver.get('https://www.mvideo.ru/')

# //div[@class="gallery-title-wrapper"]/div[contains(text(),"Хиты продаж")]

# //div[@class="gallery-layout"][@data-init="ajax-category-carousel"]

# data-init="galleryCarousel"
# ожидаем появления писем
goods = []
try:

    #       parent_hits_obj = driver.find_element_by_xpath('//div[@class="gallery-layout" and descendant::div[contains(text(), "Хиты продаж")]]//ul[@data-init="galleryCarousel"]')
    parents_hits_obj = driver.find_elements_by_xpath('//div[@class="gallery-layout"]')
    # ищем родителя у которого класс gallery-layout
    hits_obj = None
    myparent_hit = None
    # ищем именного того предка (myparent_hit) у которго потомок hits_obj содержит  "Хиты продаж"
    #
    for parent_hit in parents_hits_obj:
        try:
            # print(parent_hit.get_attribute('class'))
            # print(parent_hit)
            # print(parent_hit.find_element_by_xpath('./child::*').get_attribute('class'))
            hits_obj = parent_hit.find_element_by_xpath('.//div[contains(text(), "Хиты продаж")]')
            myparent_hit = parent_hit
        except:
            #print(hits_obj)
            pass

    if not myparent_hit:
        # мы не нашли контейнер Хиты продаж . выходим
        print('Мы не нашли контейнер Хитоы продаж . выходим')
        exit(1)

    # мы нашли контейнер Хиты продаж . продолжаем
    # ищем кнопку следующие

    next_button = myparent_hit.find_element_by_xpath('.//a[contains(@class, "next-btn")]')
    maxclick = 20
    curclick = 0


    while curclick < maxclick:
        # щелкаем на нее пока она не станет неактивной
        try:
            if 'disabled' not in next_button.get_attribute('class'):
                next_button.click()
                time.sleep(1)
            else:
                # ура. дощелкались..
                break
        except:
            # приехали..... дощелкались. что-то не так
            break
        curclick += 1

# все товары сейчас в DOMe все товары. обрабатываем .//a[@data-product-info]
    for li_good in myparent_hit.find_elements_by_xpath('.//li[contains(@class, "gallery-list-item")]'):
        good={}
        try:
            a_good=li_good.find_element_by_xpath('.//a[@data-product-info]')
            good['link']=a_good.get_attribute('href')
            dict_product=json.loads(a_good.get_attribute('data-product-info'))
            good['name'] = dict_product["productName"]
            good['price'] = dict_product["productName"]
            good['img'] = a_good.find_element_by_xpath('.//img').get_attribute('src')
            goods.append(good)
        except:
            print ("Error")

    # закрывем драйвер
    driver.close()

    # получили все товары сохраняем в базу
    # подготавливаем базу для сохранения писем
    client = MongoClient('localhost', 27017)
    db = client['goods_db']

    # создаем коллекцию  db.vacancies
    goods_col = db.goods_mvideo

    # очищаем коллекцию
    goods_col.drop()

    goods_col.insert_many(goods)


    # проверяем сколько элементов записано в базу
    print (f' Всего хитовых товаров: {len(goods)}, записано в базу: {goods_col.estimated_document_count()}')



except:
    print('увы, не удалось ввести qqqqq  . Печалька. Выходим.....')
    # закрывем драйвер
    driver.close()

