# crawler/items.py
import scrapy

class URLItem(scrapy.Item):
    url = scrapy.Field()
    server_type = scrapy.Field()
    timestamp = scrapy.Field()
    source = scrapy.Field()
    keyword = scrapy.Field()
    status_code = scrapy.Field()
    headers = scrapy.Field()
