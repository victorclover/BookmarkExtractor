# bookmark_parser.py
# Main class for parsing HTML bookmark files from browsers like Firefox/Chrome/Edge
# Author: Victor
# License: GPL-3.0

"""
Functional Design:
- Contains BookmarkParser class that handles parsing and traversal of bookmark files
- Provides methods to export directory structure, bookmarks, or both
- Uses BeautifulSoup for HTML parsing and handles nested directory structures

Exception Handling:
- Catches file I/O errors during file parsing
- Handles malformed HTML structures gracefully
- Logs errors through configured logger

Usage Guide:
1. Instantiate BookmarkParser with bookmark file path
2. Call export methods (export_directory_and_bookmarks/export_directory_structure/export_bookmarks)
3. Handle returned structured data or exceptions
"""

from bs4 import BeautifulSoup, Tag
from logger import logger
from config import DEFAULT_SHOW_BOOKMARK_NAME

class BookmarkParser:
    def __init__(self, file_path):
        """
        Initialize bookmark parser with target HTML file
        :param file_path: Path to HTML bookmark file
        :raises FileNotFoundError: If specified file doesn't exist
        """
        self.file_path = file_path
        self.tree = self._parse_file()

    def _parse_file(self):
        """
        Internal method to parse HTML file using BeautifulSoup
        :return: BeautifulSoup object representing DOM tree
        :raises Exception: For general parsing errors
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return BeautifulSoup(content, 'html5lib')
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
            raise
        except Exception as e:
            logger.error(f"Error parsing file: {e}")
            raise

    def _traverse_directory(self, directory_node, include_bookmarks=True):
        """
        Recursively traverse directory nodes to build structure
        :param directory_node: Starting DL node for traversal
        :param include_bookmarks: Whether to include bookmarks in output
        :return: List of dictionaries representing directory structure
        """
        result = []
        if not isinstance(directory_node, Tag) or directory_node.name != 'dl':
            return result
    
        for dt in directory_node.find_all('dt', recursive=False):
            h3 = dt.find('h3', recursive=False)
            a_tag = dt.find('a', recursive=False)

            if h3:  # Directory node
                folder_name = h3.get_text(strip=True)
                sub_dl = h3.find_next_sibling('dl', recursive=False)
                sub_items = self._traverse_directory(sub_dl, include_bookmarks) if sub_dl else []
                result.append({"type": "folder", "name": folder_name, "items": sub_items})                
            elif include_bookmarks and a_tag:  # Bookmark node
                bookmark_name = a_tag.get_text(strip=True)
                bookmark_url = a_tag.get('href', '').strip()
                result.append({"type": "bookmark", "name": bookmark_name, "url": bookmark_url})

        return result

    def export_directory_and_bookmarks(self, target_directory=None):
        """
        Export complete directory structure with bookmarks
        :param target_directory: Starting directory name (None for root)
        :return: Nested dictionary structure with folders/bookmarks
        :raises ValueError: If target directory not found
        """
        target = self._get_target_node(target_directory)
        return self._traverse_directory(target)

    def export_directory_structure(self, target_directory=None):
        """
        Export directory structure without bookmarks
        :param target_directory: Starting directory name (None for root)
        :return: Nested dictionary structure with folders only
        """
        target = self._get_target_node(target_directory)
        return self._traverse_directory(target, include_bookmarks=False)

    def export_bookmarks(self, target_directory=None):
        """
        Export flattened list of bookmarks
        :param target_directory: Starting directory name (None for root)
        :return: List of bookmarks (names or URLs based on config)
        """
        def flatten_bookmarks(data):
            bookmarks = []
            for item in data:
                if item.get('type') == 'folder':
                    bookmarks.extend(flatten_bookmarks(item['items']))
                elif item.get('type') == 'bookmark':
                    bookmarks.append(item['name'] if DEFAULT_SHOW_BOOKMARK_NAME else item['url'])
            return bookmarks

        result = self.export_directory_and_bookmarks(target_directory)
        return flatten_bookmarks(result)

    def _get_target_node(self, target_directory):
        """
        Helper method to find target DL node
        :param target_directory: Directory name to search for
        :return: BeautifulSoup DL node object
        """
        if target_directory is None:
            return self.tree.find('dl')
        
        target_h3 = self.tree.find('h3', text=lambda t: t and t.strip() == target_directory.strip())
        if not target_h3:
            logger.error(f"Directory '{target_directory}' not found")
            raise ValueError(f"Directory '{target_directory}' doesn't exist")
            
        target_dt = target_h3.parent
        return target_dt.find('dl', recursive=False)
    