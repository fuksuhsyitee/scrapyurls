# crawler/middlewares.py
from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import time
from utils.config import ConfigManager

class CustomRetryMiddleware(RetryMiddleware):
    def __init__(self, settings):
        super().__init__(settings)
        self.config = ConfigManager()
        self.rate_limits = self.config.rate_limits
        self.last_request_time = {}

    def process_request(self, request, spider):
        """Handle rate limiting."""
        current_time = time.time()
        domain = request.url.split('/')[2]

        if domain in self.last_request_time:
            time_passed = current_time - self.last_request_time[domain]
            if time_passed < self.rate_limits['delay_between_requests']:
                time.sleep(self.rate_limits['delay_between_requests'] - time_passed)

        self.last_request_time[domain] = current_time

class ProxyMiddleware:
    def __init__(self):
        self.config = ConfigManager()
        self.proxy_settings = self.config.proxy_settings

    def process_request(self, request, spider):
        """Add proxy to request if enabled."""
        if self.proxy_settings['enabled']:
            proxy = self._get_proxy()
            if proxy:
                request.meta['proxy'] = proxy

    def _get_proxy(self):
        """Get proxy from your proxy pool."""
        # Implement your proxy rotation logic here
        pass
