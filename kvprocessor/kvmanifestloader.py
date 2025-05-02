import os
import requests
import re
from urllib.parse import urlparse, urlunparse
from kvprocessor.kvglobalsettings import get_version_major, get_version_minor, get_version
from kvprocessor.kvprocessor import KVProcessor
from kvprocessor.util.log import log
from kvprocessor.util.errors import ManifestError
from typing import Optional

class KVManifestLoader:
    def __init__(self, file_url: str, cache_dir: str = "./struct", root: Optional[str] = None, manifest_version: str = get_version()):
        self.file_url = file_url
        self.cache_dir = cache_dir
        self.manifest_version = manifest_version
        self.root = root
        self.manifest = None
        self.namespace_overrides: dict[str, str] = {}
        self._fetch_manifest()
        self._parse_manifest()
        if int(str(self.manifest_version).strip().split(".")[1]) >= 2:
            self.validate_manifest()

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
                        if int(str(self.manifest_version).strip().split(".")[1]) >= 2:
                            if (len(line.split(":")) == 0) and (len(line.split(".")) >= 1):
                                log("Found namespace")
                                match.clear()
                                match[str(line).strip()] = str(line).strip()
                            raise ValueError(f"Invalid manifest file format in line: {line}")
                    else:
                        log("Found namespace overide")
                    key, value = match.groups()
                    log(f"Parsing Line {i} key={key}, value={value}")    
                    self.namespace_overrides[key] = value     
        except FileNotFoundError:
            print(f"Manifest file not found: {self.file_url}")
            return None

    def validate_manifest(self):
        """Validates the manifest for required fields and structure."""
        if not self.manifest:
            raise ManifestError("Manifest is not loaded.")

        for i, line in enumerate(self.manifest.splitlines(), start=1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' not in line:
                raise ManifestError(f"Invalid manifest format at line {i}: {line}")

        log("Manifest validation passed.")