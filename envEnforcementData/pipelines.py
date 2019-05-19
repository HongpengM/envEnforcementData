# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os; import os.path as osp
import logging
import pymongo
import envEnforcementData.settings as settings
from envEnforcementData.items import EnvEnforcementFileItem, EnvEnforcementRecordItem
logging.basicConfig(level=logging.INFO,
                    filemode='a',
                    filename=osp.join(settings.LOG_FOLDER, 'pipelines.log'),
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
            if possibleDuplicate:
                different_keys = []
                updated_permitted_keys = [
                    'updatedAt',
                    'pageType',
                    'pageResponse',
                    'pageResponseType',
                    'pageTable',
                    'pageAppendix'
                ]
                for k in item.keys():
                    if possibleDuplicate[k] != item[k]:
                        different_keys.append(k)
                for k in different_keys:
                    if k in updated_permitted_keys:
                        if k == 'updatedAt':
                            if (item[k] - possibleDuplicate[k]).total_seconds() < 3600:
                                break
                        possibleDuplicate[k] = item[k]
                        logger.info('[Update]:: '+
                                    ' Id:'+
                                    possibleDuplicate['_id']+
                                    ','+
                                    k+
                                    ':'+
                                    str(item[k]))
                # TODO test possibleDuplicate.save()
                possibleDuplicate.save()

        if not possibleDuplicate:
            self.db[item.collections].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
