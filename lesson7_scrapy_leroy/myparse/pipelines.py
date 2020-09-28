# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from pprint import pprint
from scrapy import Selector


class MyparsePipeline:
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.leroy_20200924

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        # doc = dict(item)
        if collection.find({'article':item['article']}).count() ==0:
            collection.insert_one(item)
        return item


# обрабатывает характеристики товара и с охраняет их в словаре

class CorrectPipeline:

    def process_item(self, item, spider):
        # обработка харакетиристик товара
        try:
            ch_dict = {}
            sel = Selector(text=item["characteristics"])
            # value[0] содержит  весь html блок c характеристиками
            for ch1 in sel.xpath('//div[@class="def-list__group"]'):
                try:
                    # парсим из характеристики названеи и значение
                    ch_dict[ch1.xpath('.//dt[@class="def-list__term"]/text()').extract_first()] = \
                        ch1.xpath('.//dd[@class="def-list__definition"]/text()').extract_first().strip()
                except:
                    pass
            item["characteristics"]=ch_dict
        except:
            pass
        # обработка цена товара - в тип float
        try:
            item['price']= float(item['price'].replace(" ", ""))
        except:
            item['price']= None  # Если цена ошибочна

        # обработка валюты
        try:
            item['currency']= "руб." if item['currency']== "₽" else item['currency']
        except:
            item['currency']= None  # Если какая то непонятная пока  ошибка

        return item






class LeroyPhotosPipeline(ImagesPipeline):
    dictphotos={} #
    def get_media_requests(self, item, info):
        if item['photos']:

            for img in item['photos']:
                try:
                    # всталяем артикул как дополнительное значение в поле  meta запроса в виде словаря в виде  {<имяПаука>_article : <артукул_товара>} напрмиер {leroy_article:'13324266'}
                    yield scrapy.Request(img, meta={self.get_article_meta(info):item['article']})
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        # проверяем поле , встравленно специльно чтобы хранить артикул в meta запроса
        if self.get_article_meta(info) in request.meta:
            # в лерой сам путь к картинке вроде хранит артикул - но вдруг они что то поменяют и тогда облом
            # создаем более универсальный вариант. Хотя мне он не очень нравится. но пока лучше не нашел.....
            # сохраняем картики в папке  <артикулТовара>/<исходноеИмяКартинки>
            targetfile = request.meta[self.get_article_meta(info)] +'/' + request.url.split('/')[-1]
        else:
            targetfile=ImagesPipeline.file_path(self,request,response,info)
        return targetfile

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]

        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")

        adapter = ItemAdapter(item)
        adapter['image_paths'] = image_paths
        return item
    # генерируем строку для meta поля в запросе
    def get_article_meta(self, info=None):
        return  (info.spider.name if info.spider.name else 'noname') + '_article'