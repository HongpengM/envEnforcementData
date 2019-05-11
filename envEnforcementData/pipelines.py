# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymongo
from envEnforcementData.items import EnvEnforcementFileItem, EnvEnforcementRecordItem

logger = logging.getLogger('*Pipeline Logger*')


class EnvenforcementdataPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoStoragePipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        possibleDuplicate = None
        if isinstance(item, EnvEnforcementRecordItem):
            possibleDuplicate = self.db[item.collections].find_one({
                'entity':
                item['entity'],
                'annouceDate':
                item['annouceDate'],
                'pageSourceWebsite':
                item['pageSourceWebsite'],
                'punishReason':
                item['punishReason']
            })
        if isinstance(item, EnvEnforcementFileItem):
            possibleDuplicate = self.db[item.collections].find_one({
                'pageLink':
                item['pageLink'],
                'pageTitle':
                item['pageTitle']
            })

        if not possibleDuplicate:
            self.db[item.collections].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
