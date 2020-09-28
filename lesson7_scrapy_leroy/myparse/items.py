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

# в данном случсе не используется - переведена в pipeline
# def correct_price(value):
#     try:
#         return float(value.replace(" ", ""))
#     except:
#         return  0

# в данном случсе не используется - переведена в pipeline
# def correct_currency(value):
#     if value=="₽":
#         return "руб."
#     else:
#         return value


class MyparseItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    article = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    currency=scrapy.Field(output_processor=TakeFirst())
    # этот варинт первоначальный и он закоментирова так как код обработка полей  перенесена в CorrectPipeline
    # price = scrapy.Field(input_processor = MapCompose(correct_price),output_processor=TakeFirst())
    # currency=scrapy.Field(input_processor = MapCompose(correct_currency),output_processor=TakeFirst())
    description= scrapy.Field()
    characteristics= scrapy.Field(output_processor = TakeFirst())
    image_paths = scrapy.Field()
    _id = scrapy.Field()  # это поле чисто для mongo который не может впихнуть _id в объект item.
                          # но может в словарь, если мы ,например, предварительно перед сохранением в базу item переведем в словарь, например dict_item=dict(item)
    pass
