from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from myparse import settings
from myparse.spiders.leroy import LeroySpider
# для устранения ошибки No Module named PIL установить библиотеку pillow
# pip install pillow



'''
3. Взять любую категорию товаров на сайте Леруа Мерлен. Собрать с использованием
ItemLoader следующие данные:
● название;
● все фото;
● параметры товара в объявлении.
4. С использованием output_processor и input_processor реализовать очистку и преобразование
данных. Цены должны быть в виде числового значения.
5. *Написать универсальный обработчик параметров объявлений, который будет формировать
данные вне зависимости от их типа и количества.
6. *Реализовать более удобную структуру для хранения скачиваемых фотографий.
'''

#------------------------------------------
# подсвечивание логов в консоли scrapy
# https://pypi.org/project/colorlog/
# ниженаписанный код  найден на https://stackoverflow.com/questions/42095184/scrapy-framework-colorize-logging
# соответствие индекса цвету смотреть https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
# код подправлен для использования 256 цветов. см файл HowUse.txt
# вставить в settings.py
# pip install colorlog

import copy

from colorlog import ColoredFormatter
import scrapy.utils.log

color_formatter = ColoredFormatter(
    (
        '%(log_color)s%(levelname)-5s%(reset)s '
        '%(c202)s[%(asctime)s]%(reset)s'
        '%(thin_c236)s %(name)s %(funcName)s %(bold_purple)s:%(lineno)d%(reset)s '
        '%(log_color)s%(message)s%(reset)s'
    ),
    datefmt='%y-%m-%d %H:%M:%S',
    # цвета брать  из раздела 8-bit  в формате с№  , с -это латинская буква с (сокращенно от color) где № число от 0 до 255   https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit
    log_colors={
        'DEBUG': 'blue',
        'INFO': 'bold_c25',
        'WARNING': 'red',
        'ERROR': 'bg_bold_red',
        'CRITICAL': 'red,bg_c244',
    }
)

_get_handler = copy.copy(scrapy.utils.log._get_handler)

def _get_handler_custom(*args, **kwargs):
    handler = _get_handler(*args, **kwargs)
    handler.setFormatter(color_formatter)
    return handler

scrapy.utils.log._get_handler = _get_handler_custom

#=========================================================



if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    # answer = input('Введите поисковый запрос')
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroySpider,params=['краска'])

    process.start()