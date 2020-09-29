# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramParserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    user_id = scrapy.Field()
    photo = scrapy.Field()
    username = scrapy.Field()
    fullname= scrapy.Field()
    node = scrapy.Field()
    subscriptions = scrapy.Field() # список на кого подписан пользователь, а кто подписан на этого пользоваиелся - нужно опрашивать базу польщователя у кого в списках полдписок есть этот пользователь
    _id = scrapy.Field()  # это поле чисто для mongo который не может впихнуть _id в объект item.
                          # но может в словарь, если мы ,например, предварительно перед сохранением в базу item переведем в словарь, например dict_item=dict(item)

    pass
