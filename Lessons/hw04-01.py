from pprint import pprint
#pip install lxml
from lxml import html
import requests
import datetime

# для удобства работы xpath можно использоать расширени для chrome: chropath

'''
Написатьприложение,которое собирает основные новости ссайтов mail.ru,lenta.ru,yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
●название источника;
●наименование новости;
●ссылку на новость;
●дата публикации.
'''



# получение новеостей с yandex.ru
def news_yandex ():
    hotnews=[]
    news_dict={}
    main_link = 'https://yandex.ru'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36' }
    response = requests.get(main_link, headers=header)
    try:

        root = html.fromstring(response.text)
#        news=root.xpath('//ul[@class="tabs-content"]/li[@class="tabs-content__item"]')
        path_hotnews = root.xpath('//ol[contains(@class, "news__list")]/li/a')
        for news in path_hotnews:
            news_dict={}
            news_dict['link']=news.xpath('@href')[0]
            news_dict['site'] = main_link
            news_dict['name'] = news.xpath('@aria-label')[0]
            news_dict['date'] = datetime.date.today()
            hotnews.append(news_dict)
#el = doc.xpath("//div[contains(@class, 'channel')]")

    except:
        print ("Ошибка запроса yandex.ru")
    return hotnews


# получение новеостей с mail.ru
def news_mail ():
    hotnews=[]
    news_dict={}
    main_link = 'https://news.mail.ru'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36' }
    response = requests.get(main_link, headers=header)
    try:

        root = html.fromstring(response.text)
        path_hotnews = root.xpath('//li[contains(@class, "list__item")]/a')
        for news in path_hotnews:
            news_dict={}
            news_dict['link']=main_link + news.xpath('@href')[0]
            news_dict['site'] = main_link
            news_dict['name'] = news.xpath('./text()')[0]
            news_dict['date'] = datetime.date.today()
            hotnews.append(news_dict)
#el = doc.xpath("//div[contains(@class, 'channel')]")

    except:
        print ("Ошибка запроса yandex.ru")
    return hotnews


# получение новеостей с lenta.ru
def news_lenta ():
    hotnews=[]
    news_dict={}
    main_link = 'https://lenta.ru'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36' }
    response = requests.get(main_link, headers=header)
    try:

        root = html.fromstring(response.text)
        path_hotnews = root.xpath('//div[@class="span8 js-main__content"]//div[@class="item"]/a')
        for news in path_hotnews:
            news_dict={}
            news_dict['link']=main_link + news.xpath('@href')[0]
            news_dict['site'] = main_link
            news_dict['name'] = news.xpath("./text()")[0]
            news_dict['date'] = news.xpath('./time/@datetime')[0].strip()
            hotnews.append(news_dict)
#el = doc.xpath("//div[contains(@class, 'channel')]")

    except:
        print ("Ошибка запроса yandex.ru")
    return hotnews




hotnews_y=news_yandex()
hotnews_m=news_mail()
hotnews_l=news_lenta()
pprint(hotnews_m+hotnews_y+hotnews_l)
