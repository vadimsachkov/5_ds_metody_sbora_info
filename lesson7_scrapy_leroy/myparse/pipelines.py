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


class MyparsePipeline:
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.leroy_20200924

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        # doc = dict(item)
        collection.insert_one(item)
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