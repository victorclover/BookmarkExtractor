# main.py
# Command-line interface for bookmark parser
# Author: Victor
# License: GPL-3.0

"""
Functional Design:
- Handles command-line argument parsing
- Coordinates parsing and output generation
- Implements formatted console output

Exception Handling:
- Catches parser exceptions and displays user-friendly messages
- Validates input parameters before processing

Usage Guide:
Run from command line with required arguments:
python main.py -f <file> [-fmt FORMAT] [-d DIRECTORY]
"""

import argparse
from bookmark_parser import BookmarkParser
from config import DEFAULT_EXPORT_FORMAT, DEFAULT_SHOW_BOOKMARK_NAME
from logger import logger

def print_hierarchical_structure(data, level=0, include_bookmarks=True):
    """
    Print nested directory structure with indentation
    :param data: Structure data from parser
    :param level: Current indentation level
    :param include_bookmarks: Whether to show bookmarks
    """
    for item in data:
        if item["type"] == "folder":
            prefix = "  " * level + "|- " if level > 0 else ""
            print(f"{prefix}{item['name']}")
            print_hierarchical_structure(item["items"], level + 1, include_bookmarks)
        elif include_bookmarks and item["type"] == "bookmark":
            prefix = "  " * level + "|- "
            display = item['name'] if DEFAULT_SHOW_BOOKMARK_NAME else item['url']
            print(f"{prefix}{display}")

def main():
    """
    Main entry point for command-line execution
    Handles argument parsing and output routing
    """
    parser = argparse.ArgumentParser(
        description='Parse browser bookmark HTML files',
        epilog='Example: python main.py -f bookmarks.html -fmt all -d "Bookmarks Bar"'
    )
    parser.add_argument('-f', '--file', required=True, 
                       help='Path to bookmark HTML file')
    parser.add_argument('-fmt', '--format', default=DEFAULT_EXPORT_FORMAT,
                       choices=['all', 'directory', 'bookmarks'],
                       help='Output format (default: %(default)s)')
    parser.add_argument('-d', '--directory', default=None,
                       help='Target directory (default: root)')

    args = parser.parse_args()
    
    try:
        bp = BookmarkParser(args.file)
        target_dir = args.directory or "Root"
        
        print(f"Target Directory: {target_dir}")
        print("Parsing Results:")
        
        if args.format == 'all':
            structure = bp.export_directory_and_bookmarks(args.directory)
            print_hierarchical_structure(structure, include_bookmarks=True)
        elif args.format == 'directory':
            structure = bp.export_directory_structure(args.directory)
            print_hierarchical_structure(structure, include_bookmarks=False)
        else:
            bookmarks = bp.export_bookmarks(args.directory)
            for bm in bookmarks:
                print(bm)
                
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()