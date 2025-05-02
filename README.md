# kvProcessor

[**PYPI Package**](https://pypi.org/project/kvprocessor/) **•** 
[**GitHub**](https://github.com/connor33341/kvProcessor) \
A Python package for processing and validating configuration dictionaries against a custom `.kv` file format.

## Installation

Install via pip:

```bash
pip install kvprocessor
```

## File format

The `.kv` file format is a simple key-value configuration format with support for type validation and default values. Each line in a `.kv` file follows this syntax:

```custom
VARIABLENAME<TYPE>:DEFAULTVALUE
```

- **VARIABLENAME**: The name of the variable.
- **TYPE**: The expected type(s) of the variable. Multiple types can be separated by `|`.
- **DEFAULTVALUE**: The default value for the variable. Use `none` if no default value is provided.
- **Comments**: Both comments as a new line, or inline are supprorted, with the `#` character.

### Example `.kv` file:
```custom
DATABASE_NAME<string>:none
DATABASE_PORT<int>:3306
ENABLE_LOGGING<bool>:true
MAX_CONNECTIONS<int|none>:none
```

## KV Manifests

A KV manifest is a file that defines namespaces and their relationships. It is used to organize and manage configurations across multiple `.kv` files. Each line in a manifest file follows this syntax:

```custom
namespace1:namespace2
```

- **namespace1**: The namespace that dosent exist as a file, but has the value as **namespace2**.
- **namespace2**: The full namespace path

### Example manifest file:
```custom
# A valid manifest
root:database
root:logging
database:connection
```

### Validating a manifest:
You can validate a manifest using the `KVManifestLoader`:

```python
from kvprocessor.kvmanifestloader import KVManifestLoader

manifest_path = "test/manifest.txt"
loader = KVManifestLoader(manifest_path)
loader.validate_manifest()  # Validates the manifest structure
```

## Config.json

The `config.json` file is used by the `KVStructLoader` to define the structure and metadata of the configuration. It includes details such as the version, root namespace, and manifest file.

### Example `config.json`:
**Note**: This example uses features from `0.1.10`, the current version is `0.2.14+`. Some extra parameters may be needed.
```json
{
    "version": "0.1.10",
    "root": "root",
    "manifest": "manifest.txt",
    "platform": "github",
    "owner": "Voxa-Communications",
    "repo": "VoxaCommunicaitons-Structures",
    "branch": "main"
}
```

### Using `KVStructLoader` with `config.json`:
```python
from kvprocessor import KVStructLoader

kv_config_url = "https://github.com/Voxa-Communications/VoxaCommunicaitons-Structures/raw/refs/heads/main/struct/config.json"
kv_struct_loader = KVStructLoader(kv_config_url)
kv_processor = kv_struct_loader.from_namespace("root.database.connection")
```

## Usage

### KVProcessor
```python
from kvprocessor import KVProcessor
from kvprocessor.kvenvloader import load_env

kv_file_path = "test/test.kv"  # Directory to .kv file
kv_processor = KVProcessor(kv_file_path)  # Create a KV processor class
kv_keys = kv_processor.return_names()  # Gets the keys (VARIBLENAME) from the .kv file
env_list = load_env(kv_keys)  # Loads all the ENV variables that match those keys
validated_config = kv_processor.process_config(env_list)  # Verifies that those env variables exist and are of the correct type
print(validated_config)
```

### KVStructLoader
```python
from kvprocessor import KVStructLoader

kv_config_url = "https://github.com/Voxa-Communications/VoxaCommunicaitons-Structures/raw/refs/heads/main/struct/config.json"
kv_struct_loader = KVStructLoader(kv_config_url)
kv_processor = kv_struct_loader.from_namespace("root.database.connection")
user_settings = {
    "DATABASE_NAME": "test_db",
    "DATABASE_PORT": 5432,
}
validated_config = kv_processor.process_config(user_settings)
print(validated_config)
```

### KVFileMerger
```python
from kvprocessor import KVFileMerger

file1 = "test/file1.kv"
file2 = "test/file2.kv"
merger = KVFileMerger(file1, file2)
merged_file = merger.merge("merged.kv")  # Merges two KV files into a new file
print(f"Merged file created at: {merged_file}")
```

### KVFileUtils
```python
from kvprocessor.kvfileutils import search_kv_files, copy_kv_file, delete_kv_file

# Search for KV files in a directory
kv_files = search_kv_files("test")
print(f"Found KV files: {kv_files}")

# Copy a KV file
copy_kv_file("test/test.kv", "test/copy_test.kv")
print("KV file copied.")

# Delete a KV file
delete_kv_file("test/copy_test.kv")
print("KV file deleted.")
```

### KVFileDiffChecker
```python
from kvprocessor import KVFileDiffChecker

file1 = "test/file1.kv"
file2 = "test/file2.kv"
diff_checker = KVFileDiffChecker(file1, file2)
differences = diff_checker.diff()
print(f"Differences between files: {differences}")
```

### KVValidator
```python
from kvprocessor import validate_kv_file

kv_file_path = "test/test.kv"
is_valid = validate_kv_file(kv_file_path)
print(f"KV file is valid: {is_valid}")
```

### Additional Data Types
The library supports additional data types such as `datetime`, `date`, `time`, and `decimal`. These can be used in `.kv` files as follows:

```custom
EVENT_DATE<datetime>:none
PRICE<decimal>:none
```

Example usage:
```python
from kvprocessor import KVProcessor

kv_file_path = "test/test.kv"  # Path to your .kv file
kv_processor = KVProcessor(kv_file_path)

# Example configuration with additional data types
config = {
    "EVENT_DATE": "2025-05-01T12:00:00",
    "PRICE": "19.99",
}

validated_config = kv_processor.process_config(config)
print(validated_config)
```

## Building
For building the library locally \
**Requires**: `python3.8+`, `pip`, `linux system` (if using the predefined shell files)

1. `git clone https://github.com/connor33341/kvProcessor.git`
2. `cd kvProcessor`
3. `bash build.sh`

`build.sh` will also install kvProcessor as a local package, which you will be able to use. If you add new features to your fork and would like them to be featured on the main repo, submit a Pull Request.

## CLI
At the current moment, there exists no documentation on this. If you would like to find usage, visit the file `kvprocessor\cli.py`. \
\
Basic Usage:
```bash
python kvprocessor/cli.py --version
```

## Library Modules
For a complete list, visit `kvprocessor\__init__.py`. A breif list of main modules, will be listed here.
 - `kvprocessor.kvprocessor`, Exports: `KVProcessor`
 - `kvprocessor.kvstructloader`, Exports: `KVStructLoader`
 - `kvprocessor.kvmanifestloader`, Exports: `KVManifestLoader`

## For the nerds
The syntax was already mentioned, however, if you would like to see how it parses, the following regex is used to determine the: `name`, `type`, and `default`:
```re
(\w+)<([\w\|]+)>:([\w+]+|none)
```
With this knowledge, you probably can figure out a way to write `.kv` files in a weird way, out of typical standard.