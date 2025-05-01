import os
import warnings
from kvprocessor.util.warnings import deprecated

def load_env(Names: list) -> dict[str, any]:
    EnvList = {}
    for Name in Names:
        Value = os.environ.get(Name)
        EnvList[Name] = Value
    return EnvList

@deprecated
def LoadEnv(Names: list) -> dict[str, any]:
    return load_env(Names)