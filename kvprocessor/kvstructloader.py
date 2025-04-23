import requests
import os
from kvprocessor.kvprocessor import KVProcessor
from kvprocessor.kvmanifestloader import KVManifestLoader
from kvprocessor.log import log

class KVStructLoader:
    def __init__(self, config_file: str, cache_dir: str = "./struct"):
        log(f"Fetching Config, from file: {config_file}")
        self.config_file = config_file
        self.cache_dir = cache_dir
        self.config = self._fetch_config()
        log(f"Config loaded: {self.config}")
        self.version = self.config["version"] if self.config else None
        self.root = self.config["root"] if self.config else None
        self.Manifest = None
        if int(str(self.version).split(".")[2]) >= 7:
            log(f"Version: {self.version} >= 7")
            self.Platform = self.config["platform"] if self.config else None
            if str(self.Platform).lower() == "github":
                self.Owner = self.config["owner"] if self.config else None
                self.Repo = self.config["repo"] if self.config else None
                self.Branch = self.config["branch"] if self.config else None
                self.Struct = self.config["struct"] if self.config else None
                self.URL = f"https://raw.githubusercontent.com/{self.Owner}/{self.Repo}/refs/heads/{self.Branch}/{self.Struct}/"
            else:
                self.URL = self.config["URL"] if self.config else None
            self.Manifest = self.config["manifest"] if self.config else None
            self.Manifest = KVManifestLoader(f"{self.URL}{self.Manifest}", self.cache_dir, self.root)
        else:
            log(f"Version: {self.version} < 7, this version has limited features")
            self.URL = self.config["URL"] if self.config else None
        
        
    def _fetch_config(self):
        try:
            response = requests.get(self.config_file)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching config file: {e}")
            return None
    
    def _fetch_kv(self, url: str, namespace: str) -> KVProcessor:
        log(f"Fetching KV file from URL: {url}")
        try:
            file_dir = os.path.join(self.cache_dir, f"{namespace}.kv")
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
        if self.Manifest:
            log(f"Using Manifest to load KVProcessor from namespace: {namespace}")
            if namespace in self.Manifest.namespace_overides:
                namespace = self.Manifest.namespace_overides[namespace]
                log(f"Namespace overridden to: {namespace}")
            else:
                log(f"Namespace not found in manifest, using original: {namespace}")
        log(f"Loading KVProcessor from namespace: {namespace}")
        if not self.config:
            raise ValueError("Config not loaded. Please check the config file URL.")
        
        orginal_namespace = namespace
        namespace = namespace.replace(f"{self.root}.", "")
        namespace = namespace.replace(".", "/")
        namespace = f"{self.URL}{namespace}.kv"
        return self._fetch_kv(namespace, orginal_namespace)
        #log(f"Loading KVProcessor from URL: {namespace}")
