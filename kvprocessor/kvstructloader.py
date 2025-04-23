import requests
import os
from kvprocessor.kvprocessor import KVProcessor
from kvprocessor.log import log

class KVStructLoader:
    def __init__(self, config_file: str, cache_dir: str = "./struct"):
        log(f"Fetching Config, from file: {config_file}")
        self.config_file = config_file
        self.cache_dir = cache_dir
        self.config = self._fetch_config()
        self.root = self.config["root"] if self.config else None
        self.URL = self.config["URL"] if self.config else None
        
    def _fetch_config(self):
        try:
            response = requests.get(self.config_file)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching config file: {e}")
            return None
    
    def _fetch_kv(self, url: str) -> KVProcessor:
        log(f"Fetching KV file from URL: {url}")
        try:
            file_dir = os.path.join(self.cache_dir, os.path.basename(url))
            log(f"Saving KV file to: {file_dir}")
            os.makedirs(os.path.dirname(file_dir), exist_ok=True)
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(file_dir, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    log(f"Writing chunk of size: {len(chunk)}")
                    file.write(chunk)
            log(f"KV file saved to: {file_dir}")
            kv_processor = KVProcessor(file_dir)
            return kv_processor
        except requests.RequestException as e:
            print(f"Error fetching KV file: {e}")
            return None
        
    def from_namespace(self, namespace: str) -> KVProcessor:
        log(f"Loading KVProcessor from namespace: {namespace}")
        if not self.config:
            raise ValueError("Config not loaded. Please check the config file URL.")
        
        namespace = namespace.replace(f"{self.root}.", "")
        namespace = namespace.replace(".", "/")
        namespace = f"{self.URL}{namespace}.kv"
        return self._fetch_kv(namespace)
        #log(f"Loading KVProcessor from URL: {namespace}")
