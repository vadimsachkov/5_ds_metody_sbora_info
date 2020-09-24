import scrapy
from scrapy.http import HtmlResponse
from myparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    # ищем ваканчии по java
    start_urls = ['https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=Java&from=suggest_post']

    def parse(self, response:HtmlResponse):
        vacancies = response.css("div.vacancy-serp-item__row_header a.bloko-link::attr(href)").extract()
        for vacancy in vacancies:
            yield response.follow(vacancy,callback=self.vacancy_parse)

        next_page = response.css("a.HH-Pager-Controls-Next::attr(href)").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def vacancy_parse(self, response:HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//p[@class='vacancy-salary']//text()").extract()
        link =  response.url
        yield JobparserItem(name=name, salary=salary, link=link)
