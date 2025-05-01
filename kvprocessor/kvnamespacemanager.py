from kvprocessor.kvmanifestloader import KVManifestLoader

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