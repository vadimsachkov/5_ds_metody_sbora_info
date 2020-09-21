from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
from pprint import pprint
from pymongo import MongoClient


def get_mail_messages(to_screen=True, to_mongo=False):
    browser_options = Options()
    browser_options.add_argument('start-maximized')

    # Chromedriver запускается без указания полного пути (MacOS Mojave)
    driver = webdriver.Chrome('./chromedriver', options=browser_options)

    try:
        driver.get('https://mail.ru/')
    except WebDriverException:
        print('\n\tОшибка! Не удается соединиться с "mail.ru"!')
        return 0, driver

    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'mailbox:login-input')))
    except TimeoutException:
        print('\n\t\tОшибка: не удалось войти в почту!')
        return 0, driver

    element.send_keys('study.ai_172')
    element.submit()

    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'mailbox:password-input')))
    except TimeoutException:
        print('\n\t\tОшибка: не удалось войти в почту!')
        return 0, driver

    element.send_keys('NextPassword172')
    element.submit()

    try:
        WebDriverWait(driver, 10).until(EC.title_contains('Входящие'))
    except TimeoutException:
        print('\n\t\tОшибка: не удалось войти в почту!')
        return 0, driver

    if to_mongo:
        client = MongoClient('127.0.0.1', 27017)
        db = client['db_mail_ru']
        mongo = db.incoming

    print('\nОбрабатывается папка "Входящие"...')

    last_message_url = None
    message_url_list = []
    while True:
        tmp_list = driver.find_elements_by_xpath('//a[contains(@class,"js-letter-list-item")]')
        last_message_element = tmp_list[-1]

        for i in range(len(tmp_list)):
            tmp_list[i] = tmp_list[i].get_attribute('href')

        if tmp_list[-1] == last_message_url:
            break

        # Удаление лишних url'ов из временного списка:
        for item in message_url_list:
            try:
                tmp_list.remove(item)
            except ValueError:
                continue

        message_url_list.extend(tmp_list)

        action = ActionChains(driver)
        action.move_to_element(last_message_element)
        action.perform()

        last_message_url = tmp_list[-1]

    print(f'\nВсего сообщений в папке "Входящие": {len(message_url_list)}')

    if to_screen:
        print('\nПочтовые сообщения:')
    else:
        print('\nСообщения обрабатываются', end='')

    write_count = 0
    for item in message_url_list:
        driver.get(item)

        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'thread__subject')))
        except TimeoutException:
            print(f'\n\t\tОшибка: не удалось загрузить сообщение ({item})!')
            return 0, driver

        message_dict = {}

        message_dict['subject'] = element.text
        message_dict['author_mail'] = driver.find_element_by_xpath(
            '//div[@class="letter__author"]/span').get_attribute('title')
        message_dict['author_name'] = driver.find_element_by_xpath('//div[@class="letter__author"]/span').text

        date = driver.find_element_by_xpath('//div[@class="letter__date"]').text.split(',')
        time_struct = time.strptime(time.ctime(time.time()), '%a %b %d %H:%M:%S %Y')
        if date[0] == 'Сегодня':
            message_dict['date'] = time.strftime('%d.%m.%Y', time_struct) + ',' + date[1]
        elif date[0] == 'Вчера':
            day = str(int(time.strftime('%d', time_struct)) - 1)
            message_dict['date'] = day + time.strftime('.%m.%Y', time_struct) + ',' + date[1]
        else:
            message_dict['date'] = ','.join(date)

        message_dict['text'] = driver.find_element_by_xpath('//div[contains(@id,"_BODY")]').text

        if to_screen:
            pprint(message_dict)

        if to_mongo:
            mongo.insert_one(message_dict)

        write_count += 1

        if write_count % 5 == 0:
            print('.', end='')

    return write_count, driver


print('\n============= Домашняя работа 5 - задание 1 =============')
print('=========================================================\n')

to_screen = None
while not to_screen:
    to_screen = input('Выводить почтовые сообщения на экран? (y/n): ').strip().lower()
    if to_screen in ['y', 'yes']:
        to_screen = True
        break
    elif to_screen in ['n', 'no']:
        to_screen = False
        break
    else:
        to_screen = None

to_mongo = None
while not to_mongo:
    to_mongo = input('Сохранять сообщения в БД? (y/n): ').strip().lower()
    if to_mongo in ['y', 'yes']:
        to_mongo = True
        break
    elif to_mongo in ['n', 'no']:
        to_mongo = False
        break
    else:
        to_mongo = None

result = get_mail_messages(to_screen=to_screen, to_mongo=to_mongo)

print('\nРезультат:')
print(f'\tВсего обработано почовых сообщений: {result[0]}')

input('\n\nНажмите любую клавишу для закрытия браузера и завершения работы...')
result[1].quit()