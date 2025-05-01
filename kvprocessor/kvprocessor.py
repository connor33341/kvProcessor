import re
from typing import Dict, Any, Union
from kvprocessor.util.log import log
from kvprocessor.util.errors import InvalidKVFileError
from kvprocessor.kvtypemap import get_type_map

class KVProcessor:
    def __init__(self, kv_file_path: str):
        self.config_spec = self._parse_kv_file(kv_file_path)

    def _parse_kv_file(self, file_path: str) -> Dict[str, dict]:
        """Parse the .kv file and return a specification dictionary."""
        spec = {}
        try:
            with open(file_path, 'r') as file:
                i = -1
                for line in file:
                    i += 1
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if line.split("#"):
                        line = line.split("#")[0].strip()
                    match = re.match(r'(\w+)<([\w\|]+)>:([\w+]+|none)', line)
                    if not match:
                        raise InvalidKVFileError(f"Invalid .kv file format in line {i + 1}: {line}")
                    key, type_str, default = match.groups()
                    types = type_str.split('|')
                    log(f"Parsing Line {i} key={key}, types={types}, default={default}")
                    spec[key] = {
                        'types': types,
                        'default': None if default == 'none' else default
                    }
            return spec
        except FileNotFoundError:
            raise FileNotFoundError(f"KV file not found: {file_path}")

    def _validate_type(self, value: Any, expected_types: list) -> bool:
        """Validate if the value matches one of the expected types."""
        type_map = get_type_map()
        for type_name in expected_types:
            if type_name not in type_map:
                raise ValueError(f"Unsupported type in .kv file: {type_name}")
            if isinstance(value, type_map[type_name]):
                return True
        return False

    def process_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Verify input dict types and apply defaults from .kv file."""
        if not isinstance(config, dict):
            raise TypeError("Input must be a dictionary")

        result = {}
        for key, spec in self.config_spec.items():
            value = config.get(key, spec['default'])
            log(f"Processing {key}: value={value}, default={spec['default']}")
            
            # If value is None (either from input or default), skip type checking
            if value is not None:
                if not self._validate_type(value, spec['types']):
                    raise TypeError(
                        f"Invalid type for {key}: expected {spec['types']}, got {type(value).__name__}"
                    )
            else:
                if spec['default'] is not None:
                    value = spec['default']
            result[key] = value

        # Check for unexpected keys in input dict
        unexpected_keys = set(config.keys()) - set(self.config_spec.keys())
        if unexpected_keys:
            raise KeyError(f"Unexpected keys in config: {unexpected_keys}")

        return result
    
    def return_names(self) -> list:
        """Return the names of the keys in the KV file."""
        return list(self.config_spec.keys())
