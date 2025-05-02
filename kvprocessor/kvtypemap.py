from typing import Any
import datetime
import decimal

type_map: dict[str, Any] = {
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
    'any': Any,
    'str': str,
    'datetime': datetime.datetime,
    'date': datetime.date,
    'time': datetime.time,
    'decimal': decimal.Decimal,
}

def get_type_map() -> dict[str, Any]:
    """
    Returns the type map for KV types.
    
    :return: A dictionary mapping KV types to Python types.
    """
    return type_map

def set_type_map(new_type_map: dict[str, Any]) -> None:
    """
    Replaces the current type map with a new one.
    
    :param new_type_map: A dictionary mapping KV types to Python types.
    """
    global type_map
    type_map = new_type_map

def add_type_map(key: str, value: Any) -> None:
    """
    Adds or overrides a single key-value pair in the type map.
    
    :param key: The key to add or override in the type map.
    :param value: The Python type to associate with the key.
    """
    type_map[key] = value

def remove_type_map(key: str) -> None:
    """
    Removes a key from the type map if it exists.
    
    :param key: The key to remove from the type map.
    """
    if key in type_map:
        del type_map[key]

def has_type_map(key: str) -> bool:
    """
    Checks if a key exists in the type map.
    
    :param key: The key to check in the type map.
    :return: True if the key exists, False otherwise.
    """
    return key in type_map

def clear_type_map() -> None:
    """
    Clears all entries in the type map.
    """
    global type_map
    type_map.clear()
