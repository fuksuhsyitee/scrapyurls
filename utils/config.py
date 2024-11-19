# utils/config.py
import yaml
import os
from pathlib import Path

class ConfigManager:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._config is None:
            self.load_config()

    def load_config(self, config_path=None):
        if config_path is None:
            config_path = os.environ.get('CRAWLER_CONFIG', 'config/crawler_config.yml')

        try:
            with open(config_path, 'r') as f:
                self._config = yaml.safe_load(f)
        except Exception as e:
            raise Exception(f"Error loading configuration: {str(e)}")

    @property
    def keywords(self):
        return self._config['crawler']['keywords']

    @property
    def mongodb_settings(self):
        return self._config['mongodb']

    @property
    def search_settings(self):
        return self._config['crawler']['search_settings']

    @property
    def proxy_settings(self):
        return self._config['crawler']['proxy_settings']

    @property
    def rate_limits(self):
        return self._config['crawler']['rate_limits']

    @property
    def logging_settings(self):
        return self._config['logging']
