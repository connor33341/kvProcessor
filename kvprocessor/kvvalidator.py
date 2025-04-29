from kvprocessor.errors import InvalidKVFileError
import re

def validate_kv_file(file_path: str) -> bool:
    """Validate the syntax of a .kv file."""
    try:
        with open(file_path, 'r') as file:
            for i, line in enumerate(file, start=1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line.split("#"):
                    line = line.split("#")[0].strip()
                match = re.match(r'(\w+)<([\w\|]+)>:([\w+]+|none)', line)
                if not match:
                    raise InvalidKVFileError(f"Invalid .kv file format in line {i}: {line}")
        return True
    except FileNotFoundError:
        raise FileNotFoundError(f"KV file not found: {file_path}")