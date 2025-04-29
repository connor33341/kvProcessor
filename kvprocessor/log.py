import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("kvprocessor.log", mode="a")
    ]
)

def log(message: str):
    logging.info(message)

def log_error(message: str):
    logging.error(message)

def log_debug(message: str):
    logging.debug(message)

def log_warning(message: str):
    logging.warning(message)