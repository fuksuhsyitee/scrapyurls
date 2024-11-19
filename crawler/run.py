# crawler/run.py
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from utils.config import ConfigManager
import logging

def setup_logging():
    config = ConfigManager()
    logging_settings = config.logging_settings
    
    logging.basicConfig(
        level=logging_settings['level'],
        format='%(asctime)s [%(levelname)s] %(message)s',
        filename=logging_settings['file'] if 'file' in logging_settings else None
    )

def main():
    # Setup logging
    setup_logging()
    
    # Get configuration
    config = ConfigManager()
    
    # Get Scrapy settings
    settings = get_project_settings()
    
    # Update settings from config
    settings.update({
        'MONGODB_URI': config.mongodb_settings['uri'],
        'MONGODB_DATABASE': config.mongodb_settings['database'],
        'MONGODB_COLLECTION': config.mongodb_settings['collection'],
        'CONCURRENT_REQUESTS_PER_DOMAIN': config.rate_limits['requests_per_domain'],
        'DOWNLOAD_DELAY': config.rate_limits['delay_between_requests'],
    })

    # Initialize the crawler process
    process = CrawlerProcess(settings)
    
    # Start the crawler with keywords from config
    process.crawl('multi_search', keywords=','.join(config.keywords))
    process.start()

if __name__ == '__main__':
    main()
