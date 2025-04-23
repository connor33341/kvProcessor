import os
import dotenv
from kvprocessor import LoadEnv, KVProcessor, KVStructLoader
dotenv.load_dotenv() # Load the .env file

def test_file():
    kv_file_path = "test/test.kv" # Directory to .kv file
    kv_processor = KVProcessor(kv_file_path) # Create a KV processor class
    kv_keys = kv_processor.return_names() # Gets the keys (VARIBLENAME) from the .kv file
    env_list = LoadEnv(kv_keys) # Loads all the ENV varibles that match those keys
    validated_config = kv_processor.process_config(env_list) # Verifies that those env varibles exist and are of the correct type
    print(validated_config)

def test_struct_loader():
    kv_struct_loader = KVStructLoader("https://github.com/Voxa-Communications/VoxaCommunicaitons-Structures/raw/refs/heads/main/struct/config.json") # Create a KVStructLoader object with the URL of the config file
    print(kv_struct_loader.root)
    print(kv_struct_loader.URL)
    kv_processor: KVProcessor = kv_struct_loader.from_namespace("voxa.api.user.user_settings") # Loads the KV file from the URL and returns a KVProcessor object
    user_settings = {
        "2FA_ENABLED": True,
        "TELEMETRY": False,
        "AGE": "25",
        "LANGUAGE": "en",
    }
    validated_config = kv_processor.process_config(user_settings) # Verifies that those env varibles exist and are of the correct type
    print(validated_config)
if __name__ == "__main__":
    test_file()
    test_struct_loader()