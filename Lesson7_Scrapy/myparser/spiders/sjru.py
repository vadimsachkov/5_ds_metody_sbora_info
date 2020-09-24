import scrapy
from scrapy.http import HtmlResponse
from myparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=java&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response:HtmlResponse):
        vacancies = response.xpath('//div [@class="Fo44F QiY08 LvoDO"]//div[@class="_3mfro PlM3e _2JVkc _3LJqf"]/a/@href').extract()
        # тоже самое но в css стиле
        # response.css('div.Fo44F.QiY08.LvoDO div._3mfro.PlM3e._2JVkc._3LJqf a::attr(href)').extract()
        for vacancy in vacancies:
            yield response.follow(vacancy,callback=self.vacancy_parse)

        next_page = response.xpath('//div[@class="_3zucV L1p51 undefined _1Fty7 _2tD21 _3SGgo"]//a[@rel="next"]/@href').extract_first()
        # тоже самое в стиле  css
        # next_page = response.css('div._3zucV.L1p51.undefined._1Fty7._2tD21._3SGgo a[rel="next"]::attr(href)').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def vacancy_parse(self, response:HtmlResponse):
        vacansy_block=response.xpath('//div[@class="_3MVeX"]')
        name = vacansy_block.xpath('.//h1/text()').extract_first()
        salary = vacansy_block.xpath('.//span[@class="_3mfro _2Wp8I PlM3e _2JVkc"]//text()').extract()
        link =  response.url
        yield JobparserItem(name=name, salary=salary, link=link)
