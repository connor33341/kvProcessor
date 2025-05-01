import os
import urllib.parse
import requests
import re
from urllib.parse import urlparse, urlunparse
from kvprocessor.kvprocessor import KVProcessor
from kvprocessor.kvstructloader import KVStructLoader
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
        self.manifest_version = KVStructLoader(urlparse(self.file_url).path.rsplit('/', 1)[0] + '/config.json', self.cache_dir).version

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
                    match: dict = re.match(r'([^:]+):([^:]+)', line)
                    if not match:
                        if str(self.manifest_version).strip().split(".")[1] >= 2:
                            if (len(line.split(":")) == 0) and (len(line.split(".") >= 1)):
                                log("Found namespace")
                                match.clear()
                                match[str(line).strip()] = str(line).strip()
                            raise ValueError(f"Invalid manifest file format in line: {line}")
                    else:
                        log("Found namespace overide")
                    key, value = match.groups()
                    log(f"Parsing Line {i} key={key}, value={value}")    
                    self.namespace_overides[key] = value     
        except FileNotFoundError:
            print(f"Manifest file not found: {self.file_url}")
            return None

class NamespaceManager:
    """Utility class for managing namespaces dynamically."""

    def __init__(self, manifest_loader: KVManifestLoader):
        self.manifest_loader = manifest_loader

    def add_namespace(self, key: str, value: str):
        """Add a new namespace to the manifest."""
        if key in self.manifest_loader.namespace_overides:
            raise ValueError(f"Namespace {key} already exists.")
        self.manifest_loader.namespace_overides[key] = value

    def remove_namespace(self, key: str):
        """Remove a namespace from the manifest."""
        if key not in self.manifest_loader.namespace_overides:
            raise KeyError(f"Namespace {key} does not exist.")
        del self.manifest_loader.namespace_overides[key]

    def list_namespaces(self) -> list:
        """List all available namespaces."""
        return list(self.manifest_loader.namespace_overides.keys())

    def update_namespace(self, key: str, new_value: str):
        """Update an existing namespace."""
        if key not in self.manifest_loader.namespace_overides:
            raise KeyError(f"Namespace {key} does not exist.")
        self.manifest_loader.namespace_overides[key] = new_value