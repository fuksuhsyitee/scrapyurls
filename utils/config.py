# utils/config.py
import yaml
import os
from pathlib import Path
import logging

class ConfigManager:
    _instance = None
    _config = None
    _keywords = None

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
            self._load_keywords()
        except Exception as e:
            raise Exception(f"Error loading configuration: {str(e)}")

    def _load_keywords(self):
        """Load keywords from the specified text file."""
        keywords_file = self._config['crawler']['keywords_file']
        
        # Handle both absolute and relative paths
        if not os.path.isabs(keywords_file):
            # If relative, assume it's relative to the config file
            config_dir = os.path.dirname(os.environ.get('CRAWLER_CONFIG', 'config/crawler_config.yml'))
            keywords_file = os.path.join(config_dir, keywords_file)

        try:
            with open(keywords_file, 'r') as f:
                # Read lines, strip whitespace, and filter out empty lines and comments
                self._keywords = [
                    line.strip() for line in f.readlines()
                    if line.strip() and not line.strip().startswith('#')
                ]
            logging.info(f"Loaded {len(self._keywords)} keywords from {keywords_file}")
        except Exception as e:
            logging.error(f"Error loading keywords file: {str(e)}")
            self._keywords = []

    @property
    def keywords(self):
        """Return the list of keywords."""
        if self._keywords is None:
            self._load_keywords()
        return self._keywords

    # ... (rest of the ConfigManager methods remain the same)
