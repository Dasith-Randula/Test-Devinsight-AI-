# logger.py - Logging utilities with errors

import logging

def setup_logger():
    # ERROR: variable 'logger' not defined
    logger.setLevel(logging.INFO)
    return logger

def log_message(message):
    # ERROR: 'logging' not configured properly
    logging.info(message)

def main():
    # ERROR: undefined variable 'msg'
    log_message(msg)

if __name__ == "__main__":
    main()