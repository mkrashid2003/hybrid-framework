import os
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

FORMATER = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")
LOG_FILE = ".\\Logs\\my_app.log"

def ensure_log_directory_exists():
    log_dir = os.path.dirname(LOG_FILE)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATER)
    return console_handler

def get_file_handler():
    ensure_log_directory_exists()  # Ensure the directory exists before creating the handler
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATER)
    return file_handler

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger
