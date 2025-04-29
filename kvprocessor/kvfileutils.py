import os
import shutil

def search_kv_files(directory: str) -> list:
    """Search for all .kv files in a directory."""
    kv_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".kv"):
                kv_files.append(os.path.join(root, file))
    return kv_files

def copy_kv_file(source: str, destination: str):
    """Copy a .kv file to a new location."""
    if not os.path.exists(source):
        raise FileNotFoundError(f"Source file not found: {source}")
    shutil.copy(source, destination)

def delete_kv_file(file_path: str):
    """Delete a .kv file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    os.remove(file_path)