# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class InstagramParserPipeline:
    def process_item(self, item, spider):
        #print(item)
        return item



class MongoPipeline:
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.instagram

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        # doc = dict(item)
        try:
            if not collection.count_documents({"user_id": item['user_id']}):
               # если не пользователя такого нет в базе то добавляем
               collection.insert_one(item)
            else:
                if len(item['subscriptions'])>1:
                    # это уже элемент  персоны (там все его подписки) - его заменяем полностью
                    collection.replace_one({"user_id": item['user_id']}, item, upsert=True)
                else:
                # такой уже есть - добавляем  подписки
                    if item['subscriptions'][0] is not None:
                        doc=collection.find_one({"user_id": item['user_id']})
                        subs=set(doc['subscriptions'] + item['subscriptions']) # объединяем подписки с базы и новые ,удаляя дубликаты
                        subs.discard(None)
                        collection.update({"user_id": item['user_id']}, {"$set":{'subscriptions':list(subs)}}, upsert=True)

        except ValueError:
            print(ValueError)

        return item
