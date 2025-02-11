# logger.py
# Logging configuration for bookmark parser
# Author: Victor
# License: GPL-3.0

"""
Functional Design:
- Configures logging handlers for both console and file output
- Creates structured log format with timestamps
- Handles log directory creation

Exception Handling:
- Catches permission errors during log file creation
- Falls back to console-only logging if file logging fails

Usage Guide:
- Import logger directly from module
- Use standard logging methods (debug(), info(), warning(), error())
"""

import logging
import os
from config import DEFAULT_LOG_LEVEL

def setup_logger(log_level=DEFAULT_LOG_LEVEL):
    """
    Configure and return application logger
    :param log_level: Minimum severity level to track
    :return: Configured Logger instance
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    try:
        os.makedirs('logs', exist_ok=True)
        file_handler = logging.FileHandler('logs/bookmark_parser.log')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except PermissionError as e:
        logger.error(f"Log file creation failed: {e}")

    return logger

logger = setup_logger()