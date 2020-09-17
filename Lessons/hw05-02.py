#pip install selenium

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

driver = webdriver.Chrome('./chromedriver.exe',options=chrome_options)

driver.get('https://www.mvideo.ru/')

#//div[@class="gallery-title-wrapper"]/div[contains(text(),"Хиты продаж")]

#//div[@class="gallery-layout"][@data-init="ajax-category-carousel"]

#data-init="galleryCarousel"
# ожидаем появления писем
goods={}
try:
    # начинаем передвигаться по письмам, чтобы
    while True:
        parent_hits_obj = driver.find_element_by_xpath('//div[@class="gallery-layout" and descendant::div[contains(text(), "Хиты продаж")]]//ul[@data-init="galleryCarousel"]')
        #hits_obj = parent_hits_obj.find_element_by_xpath('//ul[@data-init="galleryCarousel"]')
        parent_hits_obj.find_element_by_xpath('//a[@data-product-info]').get_attribute('href')
        time.sleep(1)
        mails_count = len(goods) #  запоминаем столко писем было до добавления
        for letter in mails:
            # добавим только новое письмо, если такое есть игнорим. проверяем по data-uidl-id
            addnewLetter(letter, goods)

        # ограничим кол-во писем до 100. для теста хватит
        if len(goods)> mails_count and len(goods)<10:
            action = ActionChains(driver)
            action.move_to_element(mails[-1])
            action.perform()
            time.sleep(2)
        else:
            # писем больше не прибавилось - значит все уже прочитали
            break;

except:
    print('увы, не удалось ввести qqqqq  . Печалька. Выходим.....')
    mails=None