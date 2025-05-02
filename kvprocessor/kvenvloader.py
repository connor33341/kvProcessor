import os
import warnings
from kvprocessor.util.warnings import deprecated

def load_env(Names: list, defaults: dict = None) -> dict[str, any]:
    """
    Load environment variables into a dictionary.

    Args:
        Names (list): List of environment variable names to load.
        defaults (dict): Optional dictionary of default values for environment variables.

    Returns:
        dict: A dictionary containing the environment variable names and their values.
    """
    EnvList = {}
    defaults = defaults or {}
    for Name in Names:
        Value = os.environ.get(Name, defaults.get(Name))
        if Value is None:
            warnings.warn(f"Environment variable '{Name}' is not set and no default value is provided.", UserWarning)
        EnvList[Name] = Value
    return EnvList

def validate_env(Names: list) -> None:
    """
    Validate that all required environment variables are set.

    Args:
        Names (list): List of environment variable names to validate.

    Raises:
        EnvironmentError: If any required environment variable is not set.
    """
    missing_vars = [Name for Name in Names if os.environ.get(Name) is None]
    if missing_vars:
        raise EnvironmentError(f"The following required environment variables are missing: {', '.join(missing_vars)}")

@deprecated
def LoadEnv(Names: list, defaults: dict = None) -> dict[str, any]:
    """
    Deprecated wrapper for load_env.

    Args:
        Names (list): List of environment variable names to load.
        defaults (dict): Optional dictionary of default values for environment variables.

    Returns:
        dict: A dictionary containing the environment variable names and their values.
    """
    return load_env(Names, defaults)