import logging
from kvprocessor.util.struuid import uuidv4
from kvprocessor.util.warnings import deprecated
from kvprocessor.kvglobalsettings import get_cache_dir

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"{get_cache_dir()}/logs/{uuidv4()}.log", mode="a")
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

def log_critical(message: str):
    logging.critical(message)

def log_exception(message: str):
    logging.exception(message)

@deprecated    
def log_deprecated(func):
    """
    Decorator to log when a deprecated function is called.
    """
    def wrapper(*args, **kwargs):
        log_warning(f"Deprecated function '{func.__name__}' called.")
        return func(*args, **kwargs)
    return wrapper

@deprecated
def print(message: str):
    """
    Print a message to the console and log it.
    """
    log(message)
    print(message)