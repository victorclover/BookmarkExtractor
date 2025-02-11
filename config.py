# config.py
# Global configuration settings for the bookmark parser
# Author: Victor
# License: GPL-3.0

"""
Functional Design:
- Contains application-wide configuration constants
- Centralizes settings for export formats and display options

Exception Handling:
- No explicit exception handling - values should be modified programmatically

Usage Guide:
- Import DEFAULT_* constants directly where needed
- Modify values before instantiating main parser if customization needed
"""

# Export format options: 'all', 'directory', 'bookmarks'
DEFAULT_EXPORT_FORMAT = 'directory'

# Logging level: DEBUG, INFO, WARNING, ERROR
DEFAULT_LOG_LEVEL = 'INFO'

# Display bookmark names (True) or URLs (False)
DEFAULT_SHOW_BOOKMARK_NAME = True