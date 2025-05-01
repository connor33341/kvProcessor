import os
import dotenv
import pytest
import datetime
import decimal
import subprocess
from kvprocessor import LoadEnv, KVProcessor, KVStructLoader
from kvprocessor.kvfileutils import search_kv_files, copy_kv_file, delete_kv_file
from kvprocessor.kvversionmanager import KVVersionManager
from kvprocessor.util.errors import ManifestError
from kvprocessor.kvtypemap import get_type_map
from kvprocessor.kvmanifestloader import KVManifestLoader, ManifestError
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

@pytest.fixture
def kv_processor():
    kv_file_path = "test/test.kv"  # Directory to .kv file
    return KVProcessor(kv_file_path)

@pytest.fixture
def kv_struct_loader():
    return KVStructLoader("https://github.com/Voxa-Communications/VoxaCommunicaitons-Structures/raw/refs/heads/main/struct/config.json")

def test_kv_processor_return_names(kv_processor):
    kv_keys = kv_processor.return_names()  # Gets the keys (VARIBLENAME) from the .kv file
    assert isinstance(kv_keys, list)
    assert len(kv_keys) > 0

def test_kv_processor_process_config(kv_processor):
    kv_keys = kv_processor.return_names()
    env_list = LoadEnv(kv_keys)  # Loads all the ENV variables that match those keys
    validated_config = kv_processor.process_config(env_list)  # Verifies that those env variables exist and are of the correct type
    assert isinstance(validated_config, dict)

def test_kv_struct_loader_root(kv_struct_loader):
    assert kv_struct_loader.root == "voxa"

def test_kv_struct_loader_url(kv_struct_loader):
    assert kv_struct_loader.URL.startswith("https://")

def test_kv_struct_loader_namespace(kv_struct_loader):
    kv_processor = kv_struct_loader.from_namespace("voxa.api.user.user_settings")
    user_settings = {
        "2FA_ENABLED": True,
        "TELEMETRY": False,
        "AGE": "25",
        "LANGUAGE": "en",
    }
    validated_config = kv_processor.process_config(user_settings)
    assert isinstance(validated_config, dict)
    assert validated_config["2FA_ENABLED"] is True
    assert validated_config["TELEMETRY"] is False

def test_file_operations():
    kv_files = search_kv_files("test")
    assert len(kv_files) > 0

    test_file = kv_files[0]
    copy_path = "test/copy_test.kv"
    copy_kv_file(test_file, copy_path)
    assert os.path.exists(copy_path)

    delete_kv_file(copy_path)
    assert not os.path.exists(copy_path)

def test_version_manager():
    version_manager = KVVersionManager("test/versions")

    test_file = "test/test.kv"
    versioned_file = version_manager.save_version(test_file)
    assert os.path.exists(versioned_file)

    versions = version_manager.list_versions("test.kv")
    assert len(versions) > 0

    restore_path = "test/restored_test.kv"
    version_manager.restore_version("test.kv", versions[0].split(".")[-1], restore_path)
    assert os.path.exists(restore_path)
    delete_kv_file(restore_path)

def test_additional_data_types():
    type_map = get_type_map()
    assert 'datetime' in type_map
    assert 'date' in type_map
    assert 'time' in type_map
    assert 'decimal' in type_map
    assert type_map['datetime'] == datetime.datetime
    assert type_map['decimal'] == decimal.Decimal

def test_validate_manifest():
    valid_manifest_content = """# A valid manifest
    namespace1:namespace2
    namespace3:namespace4
    """
    invalid_manifest_content = """# An invalid manifest
    namespace1 namespace2
    """

    # Write valid manifest to a temporary file
    with open("test_valid_manifest.txt", "w") as file:
        file.write(valid_manifest_content)

    # Write invalid manifest to a temporary file
    with open("test_invalid_manifest.txt", "w") as file:
        file.write(invalid_manifest_content)

    try:
        loader = KVManifestLoader("test_valid_manifest.txt", root="test")
        loader.validate_manifest()  # Should pass without exceptions

        loader = KVManifestLoader("test_invalid_manifest.txt", root="test")
        try:
            loader.validate_manifest()
        except ManifestError as e:
            assert "Invalid manifest format" in str(e)
    finally:
        os.remove("test_valid_manifest.txt")
        os.remove("test_invalid_manifest.txt")

def test_list_namespaces():
    manifest_content = """# Example manifest
    namespace1:namespace2
    namespace3:namespace4
    """

    # Write manifest to a temporary file
    with open("test_manifest.txt", "w") as file:
        file.write(manifest_content)

    try:
        loader = KVManifestLoader("test_manifest.txt", root="test")
        namespaces = loader.list_namespaces()
        assert namespaces == ["namespace1", "namespace3"]
    finally:
        os.remove("test_manifest.txt")

def test_cli_list_namespaces():
    manifest_content = """# Example manifest
    namespace1:namespace2
    namespace3:namespace4
    """

    # Write manifest to a temporary file
    with open("test_manifest.txt", "w") as file:
        file.write(manifest_content)

    try:
        result = subprocess.run(["python3", "-m", "kvprocessor.cli", "list-namespaces", "test_manifest.txt"], capture_output=True, text=True)
        assert result.returncode == 0
        assert "namespace1" in result.stdout
        assert "namespace3" in result.stdout
    finally:
        os.remove("test_manifest.txt")

if __name__ == "__main__":
    test_file()
    test_struct_loader()
    test_file_operations()
    test_version_manager()