import os

def LoadEnv(Names: list) -> dict[str, any]:
    EnvList = {}
    for Name in Names:
        Value = os.environ.get(Name)
        EnvList[Name] = Value
    return EnvList
