# crawler/settings.py
from utils.config import ConfigManager

config = ConfigManager()

BOT_NAME = 'high_performance_crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'high_performance_crawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = config.search_settings.get('max_concurrent_requests', 16)
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

# Configure a delay for requests for the same website
DOWNLOAD_DELAY = config.rate_limits['delay_between_requests']

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'crawler.middlewares.RotateUserAgentMiddleware': 400,
    'crawler.middlewares.CustomRetryMiddleware': 543,
    'crawler.middlewares.ProxyMiddleware': 410,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# Configure item pipelines
ITEM_PIPELINES = {
    'crawler.pipelines.DuplicationFilterPipeline': 300,
    'crawler.pipelines.MongoDBPipeline': 400,
}

# MongoDB settings
MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'crawler_db'
MONGODB_COLLECTION = 'urls'

# Enable and configure HTTP caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 86400
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Proxy settings
PROXY_LIST = []
PROXY_MODE = 0  # 0 = Every requests have different proxy, 1 = Take only one proxy from the list and assign it to every requests

# Search engine settings
SEARCH_ENGINES = {
    'google': 'https://www.google.com/search?q={}',
    'bing': 'https://www.bing.com/search?q={}',
    'duckduckgo': 'https://duckduckgo.com/html/?q={}',
    'yahoo': 'https://search.yahoo.com/search?p={}'
}

# Set logging level
LOG_LEVEL = config.logging_settings['level']

