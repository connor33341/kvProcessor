import kvprocessor
from kvprocessor.util.warnings import deprecated
from urllib.parse import urlparse, urlunparse

version = str(kvprocessor.__version__)
cache_dir = "./struct"

def set_version(v: str):
    """Set the version of the KVProcessor."""
    global version
    version = v

def get_version() -> str:
    """Get the version of the KVProcessor."""
    return version
def get_version_tuple() -> tuple[int, ...]:
    """Get the version of the KVProcessor as a tuple."""
    version_parts = version.split('.')
    return tuple(map(int, version_parts[:3]))
def get_version_major() -> int:
    """Get the major version of the KVProcessor."""
    return int(version.split('.')[0])
def get_version_minor() -> int:
    """Get the minor version of the KVProcessor."""
    return int(version.split('.')[1])

@deprecated
def get_config_version_from_url(url: str) -> str:
    """Get the config version of the  from a URL."""
    from kvprocessor.kvstructloader import KVStructLoader  # Local import to avoid circular dependency
    return KVStructLoader(str(urlparse(url).path.rsplit('/', 1)[0] + '/config.json')).version

def set_cache_dir(dir: str):
    """Set the cache directory for the KVProcessor."""
    global cache_dir
    cache_dir = dir

def make_cache_dir():
    """Create the cache directory for the KVProcessor."""
    import os
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    return cache_dir

def get_cache_dir() -> str:
    """Get the cache directory for the KVProcessor."""
    return cache_dir

@deprecated
def get_cache_dir_path() -> str:
    """Get the cache directory path for the KVProcessor."""
    import os
    return os.path.abspath(cache_dir)