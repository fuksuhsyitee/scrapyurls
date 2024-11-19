# manage_keywords.py
import argparse
from utils.keyword_manager import KeywordManager
import os

def main():
    parser = argparse.ArgumentParser(description='Manage crawler keywords')
    parser.add_argument('--add', nargs='+', help='Add keywords')
    parser.add_argument('--remove', nargs='+', help='Remove keywords')
    parser.add_argument('--list', action='store_true', help='List all keywords')
    parser.add_argument('--clear', action='store_true', help='Clear all keywords')
    parser.add_argument('--file', default='config/keywords.txt', help='Keywords file path')

    args = parser.parse_args()
    
    keyword_manager = KeywordManager(args.file)

    if args.add:
        keyword_manager.add_keywords(args.add)
        print(f"Added {len(args.add)} keywords")

    if args.remove:
        keyword_manager.remove_keywords(args.remove)
        print(f"Removed {len(args.remove)} keywords")

    if args.clear:
        keyword_manager.clear_keywords()
        print("Cleared all keywords")

    if args.list or args.add or args.remove or args.clear:
        keywords = keyword_manager.get_keywords()
        print("\nCurrent keywords:")
        for keyword in keywords:
            print(f"- {keyword}")

if __name__ == '__main__':
    main()
