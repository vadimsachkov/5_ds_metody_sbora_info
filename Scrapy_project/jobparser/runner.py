from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser.spiders.hhru import HhruSpider
# from jobparser.spiders.sjru import SjruSpider
from jobparser import settings


'''
1) Доработать паука в имеющемся проекте, чтобы он формировал item по структуре:
*Наименование вакансии
*Зарплата от
*Зарплата до
*Ссылку на саму вакансию
*Сайт откуда собрана вакансия
И складывал все записи в БД(любую)
'''



if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    # process.crawl(SjruSpider)

    process.start()