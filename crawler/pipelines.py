# crawler/pipelines.py
from pymongo import MongoClient
from utils.config import ConfigManager
import logging

class MongoDBPipeline:
    def __init__(self):
        self.config = ConfigManager()
        self.mongo_settings = self.config.mongodb_settings
        self.client = None
        self.db = None
        self.collection = None

    def open_spider(self, spider):
        """Initialize MongoDB connection when spider starts."""
        try:
            self.client = MongoClient(self.mongo_settings['uri'])
            self.db = self.client[self.mongo_settings['database']]
            self.collection = self.db[self.mongo_settings['collection']]
            logging.info("Successfully connected to MongoDB")
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    def process_item(self, item, spider):
        """Process and store items in MongoDB."""
        try:
            # Check for duplicates
            if not self.collection.find_one({'content_hash': item['content_hash']}):
                self.collection.insert_one(dict(item))
                logging.debug(f"Stored new item: {item['url']}")
            else:
                logging.debug(f"Duplicate content found: {item['url']}")
        except Exception as e:
            logging.error(f"Error processing item {item['url']}: {str(e)}")
        return item

    def close_spider(self, spider):
        """Clean up MongoDB connection when spider closes."""
        if self.client:
            self.client.close()
