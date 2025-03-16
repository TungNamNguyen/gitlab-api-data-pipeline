import os
import logging
from datetime import datetime
import sys
from config import LOG_LEVEL, LOG_DIR

def setup_logger(name="gitlab_api"):
    """
    Configure and return a logger with file and console handlers.
    
    Args:
        name (str): Name of the logger.
        
    Returns:
        logging.Logger: Configured logger object.
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
        
    # Create log filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f"{LOG_DIR}/gitlab_api_{timestamp}.log"
    
    # Create logger
    logger = logging.getLogger(name)
    
    # Set log level based on configuration
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Avoid adding handlers multiple times
    if not logger.handlers:
        # Create file handler
        file_handler = logging.FileHandler(log_filename)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger