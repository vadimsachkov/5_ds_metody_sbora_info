import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from myparse.items import MyparseItem


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']  # здесь указываем только имя домена без протокола

    def __init__(self,params):
        # https://leroymerlin.ru/search/?q=%D0%BA%D1%80%D0%B0%D1%81%D0%BA%D0%B0&suggest=true
        # в params[0] пеердаю первый параметр, в данном случае название нужного товара
        self.start_urls = [f'https://leroymerlin.ru/search/?q={params[0]}']

    def parse(self, response:HtmlResponse):
        good_links = response.xpath("//a[@slot='name']")
        for link in good_links:
            yield response.follow(link, callback=self.parse_good)

        next_page = response.css("a[rel='next']::attr(href)").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def parse_good(self, response:HtmlResponse):

        loader = ItemLoader(item=MyparseItem(),response = response)

        loader.add_xpath('name',"//h1[@slot='title']/text()")
        loader.add_xpath('photos','//*[@slot="media-content"]//img[@itemprop="image"]/@src')
        loader.add_xpath('article', '//uc-pdp-card-ga-enriched/@data-product-id')
        loader.add_xpath('price', '//uc-pdp-card-ga-enriched//span[@slot="price"]/text()')
        loader.add_xpath('currency', '//uc-pdp-card-ga-enriched//span[@slot="currency"]/text()')
        loader.add_xpath('characteristics', '//dl[@class="def-list"]')
        yield loader.load_item()