class KVProcessorError(Exception):
    """Base exception for KVProcessor."""
    pass

class InvalidKVFileError(KVProcessorError):
    """Raised when a .kv file has an invalid format."""
    pass

class MissingEnvironmentVariableError(KVProcessorError):
    """Raised when a required environment variable is missing."""
    pass

class NamespaceNotFoundError(KVProcessorError):
    """Raised when a namespace is not found in the manifest."""
    pass

class InvalidNamespaceError(KVProcessorError):
    """Raised when a namespace is invalid or malformed."""
    pass