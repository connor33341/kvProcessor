from kvprocessor import KVProcessor, KVStructLoader
import json

if __name__ == "__main__":
    print("Init")
    Running = True
    while Running:
        kv_struct_loader = KVStructLoader("https://github.com/Voxa-Communications/VoxaCommunicaitons-Structures/raw/refs/heads/main/struct/config.json")
        kv_processor: KVProcessor = kv_struct_loader.from_namespace(str(input("Namespace: ")))