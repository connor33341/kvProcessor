import kvprocessor
from urllib.parse import urlparse, urlunparse

version = str(kvprocessor.__version__)

def set_version(v: str):
    """Set the version of the KVProcessor."""
    global version
    version = v

def get_version() -> str:
    """Get the version of the KVProcessor."""
    return version
def get_version_tuple() -> tuple[int, int, int]:
    """Get the version of the KVProcessor as a tuple."""
    return tuple(map(int, version.split('.')))
def get_version_major() -> int:
    """Get the major version of the KVProcessor."""
    return int(version.split('.')[0])
def get_version_minor() -> int:
    """Get the minor version of the KVProcessor."""
    return int(version.split('.')[1])
@DeprecationWarning
def get_config_version_from_url(url: str) -> str:
    """Get the config version of the  from a URL."""
    from kvprocessor.kvstructloader import KVStructLoader  # Local import to avoid circular dependency
    return KVStructLoader(str(urlparse(url).path.rsplit('/', 1)[0] + '/config.json')).version