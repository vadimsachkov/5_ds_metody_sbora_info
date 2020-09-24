from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from myparser.spiders.hhru import HhruSpider
from myparser.spiders.sjru import SjruSpider
from myparser import settings


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



if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SjruSpider)

    process.start()