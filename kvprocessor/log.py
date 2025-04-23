import os

def log(message: str):
    if os.environ.get("DEBUG"):
        print(message)