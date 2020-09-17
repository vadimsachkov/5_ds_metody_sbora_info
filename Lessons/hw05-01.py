# ChromeDriver - WebDriver for Chrome https://chromedriver.chromium.org/downloads
# или  https://sites.google.com/a/chromium.org/chromedriver/home   , качаем версию равную версии установленного браузера и кладем рядом с нашими py  файлами
# просмтр версии браузера chrome  :  chrome://version/


#pip install selenium

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

driver = webdriver.Chrome('./chromedriver.exe',options=chrome_options)


'''
1. Написать программу, которая собирает входящие письма из своего или тестового почтового
ящика, и сложить информацию о письмах в базу данных (от кого, дата отправки, тема письма,
текст письма).
'''
driver.get('https://e.mail.ru/login/')

# time.sleep(2)



# так как элемент с логином находтся во фрейме то  нахим фрейм по линку и переключаемся на него
# 1-ый  вариант захода в iframe - красивый из одного оператора
try:
    frames = WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[contains(src, account.mail.ru/login)]'))
    )
except:
    print('увы  не получилось загрузить фрейм account.mail.ru/login  . Печалька. Выходим.....')
    exit(1)

# 2-ый  вариант захода в iframe - используя driver.switch_to.frame(frames)
'''
    try:
    frames = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//iframe[contains(src, account.mail.ru/login)]'))
    )
    # driver.switch_to_frame(frames)   устаревшее
    driver.switch_to.frame(frames)
except:
    print('Увы не получилось загрузить фрейм account.mail.ru/login  . Печалька. Выходим.....')
    exit(1)
    
'''

# зашли в iframe- теперь ждем подзагрузки элементов

try:
    login = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'username'))
    )
    login.send_keys('study.ai_172@mail.ru')
    login.submit()
except:
    print('увы, не удалось ввести логин  . Печалька. Выходим.....')
    exit(1)


# отлично еще не вылетели значит логин смогли ввести
# нажимаем кнопку для ввода пароля


# ожидаем поле с паролем
try:
    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'password'))
    )
    time.sleep(1)
    password.send_keys('NextPassword172')
    time.sleep(1)
    password.submit()
except:
    print('увы, не удалось ввести пароль  . Печалька. Выходим.....')
    exit(1)


# Еще не вылетели, значит мы внутри почты

# возвращаемся к главному окну
#driver.switch_to.default_content()

#driver.close()