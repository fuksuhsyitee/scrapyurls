# crawler/spiders/search_spider.py
import scrapy
from urllib.parse import urljoin, urlparse
from crawler.items import URLItem
from datetime import datetime
import json
import logging

class MultiSearchSpider(scrapy.Spider):
    name = 'multi_search'
    
    def __init__(self, keywords=None, *args, **kwargs):
        super(MultiSearchSpider, self).__init__(*args, **kwargs)
        self.keywords = keywords.split(',') if keywords else []
        self.search_engines = self.settings.get('SEARCH_ENGINES')
        self.visited_urls = set()

    def start_requests(self):
        for keyword in self.keywords:
            for engine, url_template in self.search_engines.items():
                search_url = url_template.format(keyword)
                yield scrapy.Request(
                    url=search_url,
                    callback=self.parse_search_results,
                    meta={
                        'keyword': keyword,
                        'engine': engine
                    },
                    dont_filter=True
                )

    def parse_search_results(self, response):
        keyword = response.meta['keyword']
        engine = response.meta['engine']

        # Different parsing logic for each search engine
        if engine == 'google':
            links = response.css('div.g div.r a::attr(href)').getall()
        elif engine == 'bing':
            links = response.css('li.b_algo h2 a::attr(href)').getall()
        elif engine == 'duckduckgo':
            links = response.css('a.result__url::attr(href)').getall()
        elif engine == 'yahoo':
            links = response.css('div.algo-sr a::attr(href)').getall()

        for url in links:
            if url not in self.visited_urls:
                self.visited_urls.add(url)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_url,
                    meta={
                        'keyword': keyword,
                        'engine': engine
                    },
                    errback=self.handle_error,
                    dont_filter=True
                )

    def parse_url(self, response):
        url = response.url
        server_type = self.detect_server_type(response)
        
        item = URLItem()
        item['url'] = url
        item['server_type'] = server_type
        item['timestamp'] = datetime.utcnow()
        item['source'] = response.meta['engine']
        item['keyword'] = response.meta['keyword']
        item['status_code'] = response.status
        item['headers'] = dict(response.headers)
        
        yield item

    def detect_server_type(self, response):
        headers = response.headers
        server = headers.get('Server', b'').decode('utf-8', 'ignore')
        
        if 'nginx' in server.lower():
            return 'nginx'
        elif 'apache' in server.lower():
            return 'apache'
        elif 'microsoft-iis' in server.lower():
            return 'iis'
        elif any(db_keyword in response.text.lower() for db_keyword in ['mysql', 'postgresql', 'oracle']):
            return 'database'
        else:
            return 'unknown'

    def handle_error(self, failure):
        logging.error(f"Request failed: {failure.request.url}")
