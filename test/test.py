import os
import dotenv
from kvprocessor import LoadEnv, KVProcessor, KVStructLoader
from kvprocessor.kvfileutils import search_kv_files, copy_kv_file, delete_kv_file
from kvprocessor.kvversionmanager import KVVersionManager
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

def test_file_operations():
    print("Testing file operations")
    kv_files = search_kv_files("test")
    print("Found .kv files:", kv_files)

    if kv_files:
        test_file = kv_files[0]
        copy_path = "test/copy_test.kv"
        copy_kv_file(test_file, copy_path)
        print(f"Copied {test_file} to {copy_path}")

        delete_kv_file(copy_path)
        print(f"Deleted {copy_path}")

def test_version_manager():
    print("Testing version manager")
    version_manager = KVVersionManager("test/versions")

    test_file = "test/test.kv"
    versioned_file = version_manager.save_version(test_file)
    print(f"Saved version: {versioned_file}")

    versions = version_manager.list_versions("test.kv")
    print("Available versions:", versions)

    if versions:
        restore_path = "test/restored_test.kv"
        version_manager.restore_version("test.kv", versions[0].split(".")[-1], restore_path)
        print(f"Restored version to: {restore_path}")

if __name__ == "__main__":
    test_file()
    test_struct_loader()
    test_file_operations()
    test_version_manager()