# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from pymongo.helpers import DuplicateKeyError
from scrapy.exceptions import DropItem
class TimespiderPipeline(object):
    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI', 'mongodb://127.0.0.1:27017')
        db_name = spider.settings.get('MONGODB_DB_NAME', 'ppvisual')

        self.db_client = MongoClient('mongodb://root:root@127.0.0.1:27017')
        self.db = self.db_client[db_name]

    def close_spider(self, spider):
        self.db_client.close()
    def process_item(self, item, spider):
        collection_name = item.__class__.__name__
        try:
            self.db[collection_name].insert(dict(item))
        except DuplicateKeyError:
            return DropItem("Duplicate item found: %s" % item)
        else:
            return item
