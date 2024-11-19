# utils/keyword_manager.py
import os
from pathlib import Path

class KeywordManager:
    def __init__(self, keywords_file):
        self.keywords_file = keywords_file

    def add_keywords(self, new_keywords):
        """Add new keywords to the file."""
        existing_keywords = self.get_keywords()
        # Combine existing and new keywords, remove duplicates
        all_keywords = list(set(existing_keywords + new_keywords))
        
        with open(self.keywords_file, 'w') as f:
            for keyword in sorted(all_keywords):
                f.write(f"{keyword}\n")

    def remove_keywords(self, keywords_to_remove):
        """Remove specified keywords from the file."""
        existing_keywords = self.get_keywords()
        remaining_keywords = [k for k in existing_keywords if k not in keywords_to_remove]
        
        with open(self.keywords_file, 'w') as f:
            for keyword in sorted(remaining_keywords):
                f.write(f"{keyword}\n")

    def get_keywords(self):
        """Get current list of keywords."""
        if not os.path.exists(self.keywords_file):
            return []
            
        with open(self.keywords_file, 'r') as f:
            return [line.strip() for line in f.readlines() 
                   if line.strip() and not line.strip().startswith('#')]

    def clear_keywords(self):
        """Clear all keywords from the file."""
        with open(self.keywords_file, 'w') as f:
            f.write("")
