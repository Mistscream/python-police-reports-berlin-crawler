# -*- coding: utf-8 -*-

from datetime import datetime

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class MongoPipeline(object):
    client = None
    db = None

    def __init__(self, mongo_enabled, mongo_uri, mongo_db, mongo_collection, mongo_drop_collection):
        self.mongo_enabled = mongo_enabled
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        self.mongo_drop_collection = mongo_drop_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_enabled=crawler.settings.get('SCRAPY_POLICE_REPORTS_CRAWLER_MONGO_ENABLED'),
            mongo_uri=crawler.settings.get('SCRAPY_POLICE_REPORTS_CRAWLER_MONGO_URI'),
            mongo_db=crawler.settings.get('SCRAPY_POLICE_REPORTS_CRAWLER_MONGO_DATABASE'),
            mongo_collection=crawler.settings.get('SCRAPY_POLICE_REPORTS_CRAWLER_MONGO_COLLECTION'),
            mongo_drop_collection=crawler.settings.get('SCRAPY_POLICE_REPORTS_CRAWLER_MONGO_DROP_COLLECTION')
        )

    def open_spider(self, spider):
        if self.mongo_enabled:
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]

            if self.mongo_drop_collection:
                self.db[self.mongo_collection].drop()
                print('Dropped collection')

    def close_spider(self, spider):
        if self.mongo_enabled:
            self.client.close()

    def process_item(self, item, spider):
        if self.mongo_enabled:
            item['updated'] = datetime.now()
            doc = self.db[self.mongo_collection].find_one({'url': item['url']})

            if not doc:
                item['created'] = datetime.now()
                self.db[self.mongo_collection].insert_one(dict(item))

                print('Inserted new document')
            else:
                # self.db[self.mongo_drop_collection].update_one(
                #    {'_id': doc['_id']},
                #    {'$set': dict(item)}
                # )

                print('Updated existing document')
