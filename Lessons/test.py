# ChromeDriver - WebDriver for Chrome https://chromedriver.chromium.org/downloads
# или  https://sites.google.com/a/chromium.org/chromedriver/home   , качаем версию равную версии установленного браузера и кладем рядом с нашими py  файлами
# просмтр версии браузера chrome  :  chrome://version/


# pip install selenium

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome('./chromedriver.exe', options=chrome_options)

'''
1. Написать программу, которая собирает входящие письма из своего или тестового почтового
ящика, и сложить информацию о письмах в базу данных (от кого, дата отправки, тема письма,
текст письма).
'''
driver.get('https://e.mail.ru/login/')

# time.sleep(2)

try:
    login = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'username'))
    )
    login.send_keys('study.ai_172@mail.ru')
    login.submit()
except:
    print('увы, не удалось ввести логин  . Печалька. Выходим.....')
    exit(1)

