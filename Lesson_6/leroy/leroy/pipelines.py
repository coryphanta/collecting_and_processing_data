# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from urllib.parse import urlparse

import scrapy
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class LeroyPipeline:

    def __init__(self):
        db = MongoClient('localhost', 27017)
        self.db = db.leroy_db

    def process_item(self, item, spider):
        item['desc'] = dict(zip(
            item['desc'][:len(item['desc']) // 2],
            item['desc'][len(item['desc']) // 2:]))
        collection = self.mongo_base[spider.name]
        try:
            item['_id'] = collection.count_documents({}) + 1
        except:
            item['_id'] = 1
        collection.insert_one(item)
        return item


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

        return item

    def item_completed(self, results, item, info):
        if results:
            item['photo'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return str((item['name'])) + '/' + os.path.basename(urlparse(request.url).path)
