from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instagramparser.spiders.instagram import InstagramSpider
from instagramparser import settings

'''
1)Написать приложение, которое будет проходиться по указанному списку двух и/или более пользователей и собирать данные об их подписчиках и подписках. 
2) По каждому пользователю, который является подписчиком или на которого подписан исследуемый объект нужно извлечь имя, id, фото (остальные данные по желанию). Фото можно дополнительно скачать. 
3) Собранные данные необходимо сложить в базу данных. Структуру данных нужно заранее продумать, чтобы: 
* Написать запрос к базе, который вернет список подписчиков только указанного пользователя 
* Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь
'''


# для подсвечивания логов другими цветами в ставить в runner.py
#------------------------------------------
# подсвечивание логов в консоли scrapy
# https://pypi.org/project/colorlog/
# ниженаписанный код  найден на https://stackoverflow.com/questions/42095184/scrapy-framework-colorize-logging
# соответствие индекса цвету смотреть https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
# код подправлен для использования 256 цветов. см файл HowUse.txt
# вставить в settings.py
# pip install colorlog
'''
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

#========================================================='''






if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstagramSpider)
    process.start()


    # !!!!!!!!!!!!!!  ДЛЯ ВЫВОДА ПОЛДПИСЧИКОВ И ПОДПИСОК ЗАПУСТИТЬ print_subcribers.py