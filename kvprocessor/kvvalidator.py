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

def validate_kv_key(key: str) -> bool:
    """Validate a single key in a .kv file."""
    match = re.match(r'(\w+)<([\w\|]+)>:([\w+]+|none)', key)
    if not match:
        raise InvalidKVFileError(f"Invalid key format: {key}")
    return True

def validate_kv_value(value: str, expected_types: list) -> bool:
    """Validate a value against expected types."""
    type_map = {
        'string': str,
        'int': int,
        'float': float,
        'bool': bool,
        'none': type(None),
        'list': list,
        'dict': dict,
        'tuple': tuple,
        'set': set,
        'object': object,
        'any': object,
        'str': str
    }
    for type_name in expected_types:
        if type_name not in type_map:
            raise ValueError(f"Unsupported type: {type_name}")
        if isinstance(value, type_map[type_name]):
            return True
    return False