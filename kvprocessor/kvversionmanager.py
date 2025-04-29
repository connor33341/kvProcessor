import os
import shutil
from datetime import datetime

class KVVersionManager:
    """Manages versions of .kv files."""

    def __init__(self, version_dir: str = "./versions"):
        self.version_dir = version_dir
        os.makedirs(self.version_dir, exist_ok=True)

    def save_version(self, file_path: str):
        """Save a version of the .kv file with a timestamp."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = os.path.basename(file_path)
        versioned_file = os.path.join(self.version_dir, f"{file_name}.{timestamp}")
        shutil.copy(file_path, versioned_file)
        return versioned_file

    def list_versions(self, file_name: str) -> list:
        """List all saved versions of a .kv file."""
        versions = []
        for file in os.listdir(self.version_dir):
            if file.startswith(file_name):
                versions.append(file)
        return sorted(versions)

    def restore_version(self, file_name: str, timestamp: str, restore_path: str):
        """Restore a specific version of a .kv file."""
        versioned_file = os.path.join(self.version_dir, f"{file_name}.{timestamp}")
        if not os.path.exists(versioned_file):
            raise FileNotFoundError(f"Version not found: {versioned_file}")
        shutil.copy(versioned_file, restore_path)