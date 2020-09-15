'''ДОМАШНЕЕ ЗАДАНИЕ К УРОКУ 4.'''
'''Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
● название источника;
● наименование новости;
● ссылку на новость;
● дата публикации.'''
# pip install lxml

from pprint import pprint
from lxml import html
import requests
import time

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
req_to_mail = 'https://mail.ru/'
response = requests.get(req_to_mail)
dom = html.fromstring(response.text)
names = dom.xpath('//li[class="tabs-content__item svelte-1mkyub8"]')
pprint(names)