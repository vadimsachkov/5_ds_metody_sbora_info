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
                    # сохранякем в словаре dictphotos путь до картинки как ключ, а значение артикул товара, к которому относится картинка
                    # интересно а если картинка будет принадлежать разным  товарам, тогда что? жопа наверно
                    self.dictphotos[img]=item['article']
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        if request.url in self.dictphotos:
            # достаем ранее сохранненый артикул товара из словаря  dictphotos по ключу - href картинки
            targetfile = self.dictphotos[request.url] +'/' + request.url.split('/')[-1]
            del self.dictphotos[request.url] # удаляю эелемент словаря -он уже не нужен (оставлять не хочется, чтобы память не мусорить)
        else:
            targetfile=ImagesPipeline.file_path(self,request,response,info)
        # targetfile = request.url.split('/')[-1]
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

