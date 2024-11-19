# crawler/pipelines.py
import pymongo
from scrapy.exceptions import DropItem
import logging

class DuplicationFilterPipeline:
    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        if item['url'] in self.urls_seen:
            raise DropItem(f"Duplicate item found: {item['url']}")
        self.urls_seen.add(item['url'])
        return item

class MongoDBPipeline:
    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DATABASE'),
            mongo_collection=crawler.settings.get('MONGODB_COLLECTION')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # Create indexes for better query performance
        self.db[self.mongo_collection].create_index([('url', pymongo.ASCENDING)], unique=True)
        self.db[self.mongo_collection].create_index([('server_type', pymongo.ASCENDING)])
        self.db[self.mongo_collection].create_index([('keyword', pymongo.ASCENDING)])

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            self.db[self.mongo_collection].insert_one(dict(item))
        except pymongo.errors.DuplicateKeyError:
            spider.logger.debug(f"Duplicate URL found in MongoDB: {item['url']}")
            raise DropItem(f"Duplicate item found: {item['url']}")
        return item
