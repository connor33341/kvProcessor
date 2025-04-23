import os
import requests
import re
from kvprocessor.kvprocessor import KVProcessor
from kvprocessor.log import log

class KVManifestLoader:
    def __init__(self, file_url: str, cache_dir: str = "./struct", root: str = None):
        self.file_url = file_url
        self.cache_dir = cache_dir
        self.root = root
        self.manifest = None
        self.namespace_overides = {}
        self._fetch_manifest()
        self._parse_manifest()

    def _fetch_manifest(self):
        try:
            file_dir = os.path.join(self.cache_dir, f"{self.root}.txt")
            log(f"Saving Manifest file to: {file_dir}")
            os.makedirs(os.path.dirname(file_dir), exist_ok=True)
            response = requests.get(self.file_url, stream=True)
            response.raise_for_status()

            with open(file_dir, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    log(f"Writing chunk of size: {len(chunk)}")
                    file.write(chunk)
            
        except requests.RequestException as e:
            print(f"Error fetching manifest file: {e}")
            return None
        
    def _parse_manifest(self):
        try:
            with open(os.path.join(self.cache_dir, f"{self.root}.txt"), 'r') as file:
                self.manifest = file.read()
                log(f"Manifest loaded: {self.manifest}")
                i = -1
                for line in self.manifest.splitlines():
                    i += 1
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    match = re.match(r'([^:]+):([^:]+)', line)
                    if not match:
                        raise ValueError(f"Invalid manifest file format in line: {line}")
                    key, value = match.groups()
                    log(f"Parsing Line {i} key={key}, value={value}")    
                    self.namespace_overides[key] = value     
        except FileNotFoundError:
            print(f"Manifest file not found: {self.file_url}")
            return None