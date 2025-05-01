import re
from kvprocessor.util.errors import InvalidKVFileError
from kvprocessor.kvtypemap import get_type_map
from kvprocessor.util.warnings import deprecated

class KVFileValidator():
    def __init__(self):
        self.file_path: str = None

    def validate_kv_file(self, file_path: str) -> bool:
        if self.file_path is None:
            self.file_path = file_path
        try:
            with open(self.file_path, 'r') as file:
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
            raise FileNotFoundError(f"KV file not found: {self.file_path}")

    def validate_kv_key(self, key: str) -> bool:
        """Validate a single key in a .kv file."""
        match = re.match(r'(\w+)<([\w\|]+)>:([\w+]+|none)', key)
        if not match:
            raise InvalidKVFileError(f"Invalid key format: {key}")
        return True

    def validate_kv_value(self, value: str, expected_types: list) -> bool:
        """Validate a value against expected types."""
        type_map = get_type_map()
        for type_name in expected_types:
            if type_name not in type_map:
                raise ValueError(f"Unsupported type: {type_name}")
            if isinstance(value, type_map[type_name]):
                return True
        return False

@deprecated   
def validate_kv_file(file_path: str) -> bool:
    """Validate the syntax of a .kv file."""
    return KVFileValidator().validate_kv_file(file_path)

@deprecated
def validate_kv_key(key: str) -> bool:
    return KVFileValidator().validate_kv_key(key)

@deprecated
def validate_kv_value(value: str, expected_types: list) -> bool:
    return KVFileValidator().validate_kv_value(value, expected_types)