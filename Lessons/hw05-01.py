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
from selenium.webdriver.common.action_chains import ActionChains
import time
from pymongo import MongoClient
from pprint import pprint

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome('./chromedriver.exe',options=chrome_options)


'''
1. Написать программу, которая собирает входящие письма из своего или тестового почтового
ящика, и сложить информацию о письмах в базу данных (от кого, дата отправки, тема письма,
текст письма).
'''

# добавление в словарь нового письма
def addnewLetter(letter, letters):
    uidl = letter.get_attribute('data-uidl-id')
    # если нет такого пиьма в словаре то добавить . если такое есть игнорим. проверяем по data-uidl-id
    if uidl not in letters:
        dict = {}
        dict['uidl'] = uidl
        dict['link'] = letter.get_attribute('href')
        dict['mailfrom'] = letter.find_element_by_xpath('//span[@class="ll-crpt"]').get_attribute('title')
        dict['maildata'] = letter.find_element_by_xpath('//div[contains(@class,"llc__item_date")]').get_attribute('title')
        dict['mailsubject'] = letter.find_element_by_xpath('//span[contains(@class,"llc__subject")]').text
        letters[uidl]=dict


# вариант добавления через replace_one
def add_to_db_letter(letter, mail_col):
    try:
        mail_col.replace_one({'uidl': letter['uidl']}, letter, upsert=True)
    except ValueError:
        print(ValueError)


# подготавливаем базу для сохранения писем
client = MongoClient( 'localhost' , 27017 )
db = client[ 'letters_db' ]

# создаем коллекцию  db.vacancies
mail_col = db.mail

# очищаем коллекцию
mail_col.drop()



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


# ожидаем появления писем
letters={}
try:
    mails = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="dataset__items"]//a[@data-uidl-id]'))
    )

    # начинаем передвигаться по письмам, чтобы
    while True:
        mails = driver.find_elements_by_xpath('//div[@class="dataset__items"]//a[@data-uidl-id]')
        time.sleep(1)
        mails_count = len(letters) #  запоминаем столко писем было до добавления
        for letter in mails:
            # добавим только новое письмо, если такое есть игнорим. проверяем по data-uidl-id
            addnewLetter(letter, letters)

        # ограничим кол-во писем до 100. для теста хватит
        if len(letters)> mails_count and len(letters)<10:
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

# печатаем например первый элемент нашего словаря
letters[list(letters)[0]]

if (len(letters)):
    # собрали все письма без текста письма. теперь пора получать тело
    for key in letters:
        try:
            driver.get(letters[key]['link'])
            time.sleep(2)
            letters[key]['body']=''
            letters[key]['body']=driver.find_element_by_class_name('letter-body__body').text
            print(letters[key]['body'])
            # сохраянем письмо в базу mongodb
            add_to_db_letter(letters[key], mail_col)
        except:
            print(f'увы, не удалось прочитать письмо {key}')
# печатаем тело письма одного из элемента
# закрывем драйвер
driver.close()

# проверяем сколько элементов записано в базу
print (f' Всего прочитано писем: {len(letters)}, записано в базу: {mail_col.estimated_document_count()}')

#Читаем первое письмо из базы
pprint(mail_col.find()[0])

