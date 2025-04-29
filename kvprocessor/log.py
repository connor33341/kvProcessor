import os

def log(message: str):
    if os.environ.get("DEBUG"):
        print(f"INFO: {message}")

def log_error(message: str):
    print(f"ERROR: {message}")

def log_debug(message: str):
    if os.environ.get("DEBUG"):
        print(f"DEBUG: {message}")