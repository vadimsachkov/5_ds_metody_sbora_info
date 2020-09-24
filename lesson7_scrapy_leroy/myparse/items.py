# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from itemloaders.processors import MapCompose, TakeFirst

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
    characteristics= scrapy.Field()
    image_paths = scrapy.Field()
    _id = scrapy.Field()  # это поле число для mongo который не может впихнуть _id в объект item
    pass
