import io
import os
import requests

def download_file(url: str, destination: str):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, 'wb') as fetched_file:
        for chunk in response.iter_content(chunk_size=8192):
            fetched_file.write(chunk)