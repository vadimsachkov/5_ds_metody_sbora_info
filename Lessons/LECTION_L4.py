'''ДОМАШНЕЕ ЗАДАНИЕ К УРОКУ 4.'''
'''Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
● название источника;
● наименование новости;
● ссылку на новость;
● дата публикации.'''
# pip install lxml
# pip install requests

from pprint import pprint
from lxml import html
import requests
import datetime

# получение новеостей с russian.rt.com
def news_rt():
    newsfeed=[]
    news_dict = {}
    main_link = 'https://russian.rt.com'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
    response = requests.get(main_link, headers=header)
    try:
        root = html.fromstring(response.text)
        path_newsfeed = root.xpath('//ul[contains(@class, "listing__rows_main-news")]/li')
        for news in path_newsfeed:
            news_dict = {}
            news_dict['link'] = main_link + ''.join(news.xpath('.//a/@href'))
            news_dict['site'] = main_link
            news_dict['name'] = news.xpath('.//a/text()')[0].strip()
            #news_dict['date'] = news.xpath('.//*/text()')[0].strip()
            news_dict['date'] = ''.join(news.xpath('.//div[contains(@class,"card__date")]/text()')).strip()
            newsfeed.append(news_dict)
    except:
        print("Ошибка запроса russian.rt.com")
    return newsfeed
newsfeed_rt = news_rt()
pprint(newsfeed_rt)

