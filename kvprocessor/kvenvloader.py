import os

def load_env(Names: list) -> dict[str, any]:
    EnvList = {}
    for Name in Names:
        Value = os.environ.get(Name)
        EnvList[Name] = Value
    return EnvList

def LoadEnv(Names: list) -> dict[str, any]:
    print("Using depricated function, update to load_env")
    return load_env(Names)