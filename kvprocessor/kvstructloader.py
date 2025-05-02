import requests
import os
import shutil
from pathlib import Path
from kvprocessor.kvprocessor import KVProcessor
from kvprocessor.kvmanifestloader import KVManifestLoader
from kvprocessor.util.log import log
from kvprocessor.util.errors import NamespaceNotFoundError, InvalidNamespaceError, ManifestError, ConfigFetchError, KVFetchError
from kvprocessor.kvglobalsettings import get_version

class KVStructLoader:
    def __init__(self, config_file: str, cache_dir: str = "./struct"):
        log(f"Fetching Config, from file: {config_file}")
        self.config_file = config_file
        self.cache_dir = cache_dir
        if os.path.exists(self.cache_dir):
            log(f"Cache directory exists: {self.cache_dir}, clearing")
            shutil.rmtree(self.cache_dir)
        self.config = self._fetch_config()
        log(f"Config loaded: {self.config}")
        self.validate_config()
        self.version = self.config["version"]
        self.root = self.config["root"]
        self.Manifest = None
        self.manifest_version = None
        if int(str(self.version).split(".")[2]) >= 7:
            log(f"Version: {self.version} >= 7")
            self.Platform = self.config.get("platform")
            if str(self.Platform).lower() == "github":
                self.Owner = self.config.get("owner")
                self.Repo = self.config.get("repo")
                self.Branch = self.config.get("branch")
                self.Struct = self.config.get("struct")
                self.URL = f"https://raw.githubusercontent.com/{self.Owner}/{self.Repo}/refs/heads/{self.Branch}/{self.Struct}/"
                if (int(str(self.version).split(".")[1]) >= 2) and (int(str(self.version).split(".")[2]) >= 14):
                    print("Using latest manifest attr")
                    self.manifest_version = self.config.get("manifest_version")
                    if not self.manifest_version:
                        raise ManifestError("Manifest version is missing in the configuration. Add tag 'manifest_version' to the config. 0.2.14+")
            else:
                self.URL = self.config.get("URL")
            manifest_file = self.config.get("manifest")
            if manifest_file:
                self.Manifest = KVManifestLoader(f"{self.URL}{manifest_file}", self.cache_dir, self.root, self.manifest_version or get_version())
            else:
                raise ManifestError("Manifest file is missing in the configuration.")
        else:
            log(f"Version: {self.version} < 7, this version has limited features")
            self.URL = self.config.get("URL")
        
    def _fetch_config(self):
        try:
            response = requests.get(self.config_file)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ConfigFetchError(f"Error fetching config file: {e}")
    
    def _fetch_kv(self, url: str, namespace: str) -> KVProcessor:
        log(f"Fetching KV file from URL: {url}")
        try:
            file_dir = os.path.join(self.cache_dir, f"{namespace}.kv")
            file_path = Path(file_dir)
            if file_path.exists():
                with open(file_path, 'r') as file:
                    log(f"KV file already exists, loading from: {file_dir}")
                    return KVProcessor(file_dir)
            log(f"Saving KV file to: {file_dir}")
            os.makedirs(os.path.dirname(file_dir), exist_ok=True)
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(file_dir, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    log(f"Writing chunk of size: {len(chunk)}")
                    file.write(chunk)
            log(f"KV file saved to: {file_dir}")
            return KVProcessor(file_dir)
        except requests.RequestException as e:
            raise KVFetchError(f"Error fetching KV file: {e}")
        
    def from_namespace(self, namespace: str) -> KVProcessor:
        if not namespace or not isinstance(namespace, str):
            raise InvalidNamespaceError("Namespace must be a non-empty string.")
        
        if self.Manifest:
            log(f"Using Manifest to load KVProcessor from namespace: {namespace}")
            if namespace in self.Manifest.namespace_overrides:
                namespace = self.Manifest.namespace_overrides[namespace]
                log(f"Namespace overridden to: {namespace}")
            else:
                log(f"Namespace not found in manifest, using original: {namespace}")
                log(f"Loading KVProcessor from namespace: {namespace}")
        if not self.config:
            raise ConfigFetchError("Config not loaded. Please check the config file URL.")
        
        original_namespace = namespace
        namespace = namespace.replace(f"{self.root}.", "")
        namespace = namespace.replace(".", "/")
        namespace = f"{self.URL}{namespace}.kv"
        return self._fetch_kv(namespace, original_namespace)

    def validate_config(self):
        """Validates the loaded configuration for required fields."""
        required_fields = ["version", "root"]
        for field in required_fields:
            if field not in self.config:
                raise ConfigFetchError(f"Missing required field in config: {field}")
        log("Configuration validation passed.")

    def clear_cache(self):
        """Clears the cache directory."""
        if os.path.exists(self.cache_dir):
            log(f"Clearing cache directory: {self.cache_dir}")
            shutil.rmtree(self.cache_dir)
        else:
            log(f"Cache directory does not exist: {self.cache_dir}")

    def get_manifest_details(self):
        """Retrieves details about the manifest."""
        if not self.Manifest:
            raise ManifestError("Manifest is not loaded.")
        log(f"Manifest details: {self.Manifest}")
        return self.Manifest

    def list_available_namespaces(self) -> list:
        """List all available namespaces from the manifest."""
        if not self.Manifest:
            raise ManifestError("Manifest is not loaded.")
        return list(self.Manifest.namespace_overrides.keys())
