import requests
from pprint import pprint
from lxml import html
from pymongo import MongoClient
import time


def get_recent_news(source):
    headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/85.0.4183.102 Safari/537.36'}

    if source == 'lenta.ru':
        url_main = 'https://lenta.ru'
        mongo = db.lenta_ru
        db_write_count = 0

        response = requests.get(url_main, headers=headers)

        if response.ok:
            document = html.fromstring(response.text)

            tag_div_item_news_list = document.xpath("//div[@class='span8 js-main__content']//div[@class='first-item']|"
                                                    "//div[@class='span8 js-main__content']//div[@class='item']")

            for item in tag_div_item_news_list:
                news_item_dict = {
                    'source': source
                }

                if ''.join(item.xpath("./@class")) == 'first-item':
                    news_item_dict['heading'] = ''.join(item.xpath("./h2/a/text()")).strip().replace('\xa0', ' ')
                    news_item_dict['url'] = url_main + ''.join(item.xpath("./h2/a/@href")).strip()
                    news_item_dict['date_time'] = ''.join(item.xpath("./h2/a/time/@datetime")).strip()
                else:
                    news_item_dict['heading'] = ''.join(item.xpath("./a/text()")).strip().replace('\xa0', ' ')
                    news_item_dict['url'] = url_main + ''.join(item.xpath("./a/@href")).strip()
                    news_item_dict['date_time'] = ''.join(item.xpath("./a/time/@datetime")).strip()

                # Проверка: находиться ли новость уже в БД?
                if mongo.find_one({'url': news_item_dict['url']}):
                    continue

                pprint(news_item_dict)
                mongo.insert_one(news_item_dict)
                db_write_count += 1

            return db_write_count, mongo.count_documents({})
        else:
            raise Exception(f'Соединиться с "{source}" не удалось!')

    elif source == 'yandex.ru':
        url_main = 'https://yandex.ru/news/'
        mongo = db.yandex_ru
        db_write_count = 0

        response = requests.get(url_main, headers=headers)

        if response.ok:
            document = html.fromstring(response.text)

            tag_div_item_news_list = document.xpath("//div[contains(@class,'news-top-stories')]//article")

            for item in tag_div_item_news_list:
                news_item_dict = {}

                if 'news-card_double' in ''.join(item.xpath("./@class")):
                    news_item_dict['heading'] = ''.join(item.xpath("./div/a/h2/text()")).strip()
                    news_item_dict['url'] = ''.join(item.xpath("./div/a/@href")).strip()
                else:
                    news_item_dict['heading'] = ''.join(item.xpath("./a/h2/text()")).strip()
                    news_item_dict['url'] = ''.join(item.xpath("./a/@href")).strip()

                # Проверка: находиться ли новость уже в БД? (здесь сравнение по заголовку)
                if mongo.find_one({'heading': news_item_dict['heading']}):
                    continue

                time_struct = time.strptime(time.ctime(time.time()), '%a %b %d %H:%M:%S %Y')

                news_item_time = ''.join(item.xpath(".//span[@class='mg-card-source__time']/text()")).strip().split()
                if news_item_time[0] == 'вчера':
                    day = str(int(time.strftime('%d', time_struct))-1)
                    news_item_dict['date_time'] = day + time.strftime('.%m.%Y ', time_struct) + news_item_time[2]
                else:
                    news_item_dict['date_time'] = time.strftime('%d.%m.%Y ', time_struct) + news_item_time[0]

                news_item_dict['source'] = ''.join(item.xpath(".//span[@class='mg-card-source__source']/a/text()")).strip()

                pprint(news_item_dict)
                mongo.insert_one(news_item_dict)
                db_write_count += 1

            return db_write_count, mongo.count_documents({})
        else:
            raise Exception(f'Соединиться с "{source}" не удалось!')

    elif source == 'mail.ru':
        url_main = 'https://news.mail.ru/'
        mongo = db.mail_ru
        db_write_count = 0

        response = requests.get(url_main, headers=headers)

        if response.ok:
            document = html.fromstring(response.text)

            to_news_rel_url_list = document.xpath(
                "//div[contains(@class,'daynews__item')]/a/@href|"
                "//div[contains(@class,'daynews ')]/../ul/li[@class='list__item']/a/@href")

            for link in to_news_rel_url_list:
                if link[0] == '/':
                    link = url_main[:-1] + link

                # Проверка: находиться ли новость уже в БД?
                if mongo.find_one({'url': link}):
                    continue

                response = requests.get(link, headers=headers)

                if response.ok:
                    document = html.fromstring(response.text)

                    news_item_dict = {}

                    news_item_dict['heading'] = ''.join(document.xpath("//div[@data-news-id]//h1/text()")).strip()
                    news_item_dict['url'] = link
                    news_item_dict['date_time'] = ''.join(document.xpath(
                        "//div[@data-news-id]//span[@datetime]/@datetime")).strip().replace('T', ' ')
                    news_item_dict['source'] = ''.join(document.xpath("//div[@data-news-id]//a[@target]/span/text()")).strip()

                    pprint(news_item_dict)
                    mongo.insert_one(news_item_dict)
                    db_write_count += 1
                else:
                    raise Exception(f'Соединиться со страницей "{link}" не удалось!'
                                    f'(Добавлено новостей в БД: {db_write_count})')
            return db_write_count, mongo.count_documents({})

        else:
            raise Exception(f'Соединиться с "{source}" не удалось!')
    else:
        raise Exception(f'Сбор новостей с сайта "{source}" пока не реализован!')


print('\n============= Домашняя работа 4 =============')
print('=============================================')

client = MongoClient('127.0.0.1', 27017)
db = client['db_news']

source_list = ['lenta.ru', 'yandex.ru', 'mail.ru']

for source in source_list:
    print(f'\nПоиск по "{source}":')
    try:
        count = get_recent_news(source)
    except Exception as error:
        print('\n\tОшибка!', error)
    else:
        print(f'\n\tПоиск выполнен. Добавлено новостей в БД: {count[0]}; '
              f'всего новостей из "{source}" в БД: {count[1]}')