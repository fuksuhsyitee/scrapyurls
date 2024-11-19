# utils/helpers.py
import requests
from urllib.parse import urlparse
import socket
import logging

class URLValidator:
    @staticmethod
    def is_valid_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    @staticmethod
    def check_url_accessibility(url, timeout=5):
        try:
            response = requests.head(url, timeout=timeout)
            return response.status_code < 400
        except:
            return False

class ProxyValidator:
    @staticmethod
    def validate_proxy(proxy, test_url="http://www.google.com", timeout=10):
        try:
            response = requests.get(
                test_url,
                proxies={"http": proxy, "https": proxy},
                timeout=timeout
            )
            return response.status_code == 200
        except:
            return False

class ServerAnalyzer:
    @staticmethod
    def get_server_info(url):
        try:
            parsed_url = urlparse(url)
            ip = socket.gethostbyname(parsed_url.netloc)
            return {
                'ip': ip,
                'hostname': parsed_url.netloc,
                'port': parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
            }
        except Exception as e:
            logging.error(f"Error analyzing server: {str(e)}")
            return None
