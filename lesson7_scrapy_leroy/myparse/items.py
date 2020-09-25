# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from itemloaders.processors import MapCompose, TakeFirst
from scrapy import Selector

def refactor_link(value):
    if value:
        return value.upper()

def correct_price(value):
    try:
        return float(value)
    except:
        return  0

def correct_currency(value):
    if value=="₽":
        return "руб."
    else:
        return value

def characteristics_parse(value):
    print(value)
    ch_dict={}
    sel=Selector(text=value[0])
    # value[0] содержит  весь html блок c характеристиками
    for ch1 in sel.xpath('//div[@class="def-list__group"]'):
        try:
            # парсим из характеристики названеи и значение
            ch_dict[ch1.xpath('.//dt[@class="def-list__term"]/text()').extract_first()] = \
                ch1.xpath('.//dd[@class="def-list__definition"]/text()').extract_first().strip()
        except:
            pass
    return ch_dict



class MyparseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # name = scrapy.Field(output_processor=TakeFirst())
    # photos = scrapy.Field(input_processor = MapCompose(refactor_link))
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    article = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor = MapCompose(correct_price),output_processor=TakeFirst())
    currency=scrapy.Field(input_processor = MapCompose(correct_currency),output_processor=TakeFirst())
    description= scrapy.Field()
    characteristics= scrapy.Field(input_processor = characteristics_parse,output_processor=TakeFirst())
    image_paths = scrapy.Field()
    _id = scrapy.Field()  # это поле число для mongo который не может впихнуть _id в объект item
    pass
