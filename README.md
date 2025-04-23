# kvProcessor

[**PYPI Package**](https://pypi.org/project/kvprocessor/) \
A Python package for processing and validating configuration dictionaries against a custom `.kv` file format.

## Installation

Install via pip:

```bash
pip install kvprocessor
```

## File format

```custom
VARIBLENAME<TYPE>:DEFAULTVAULE
```

## Usage

```python
from kvprocessor import LoadEnv, KVProcessor

kv_file_path = "test/test.kv" # Directory to .kv file
kv_processor = KVProcessor(kv_file_path) # Create a KV processor class
kv_keys = kv_processor.return_names() # Gets the keys (VARIBLENAME) from the .kv file
env_list = LoadEnv(kv_keys) # Loads all the ENV varibles that match those keys
validated_config = kv_processor.process_config(env_list) # Verifies that those env varibles exist and are of the correct type
print(validated_config)
```

This example mimics the one found in the `/test` directory. With the kv file of:
```custom
# This is a comment
DATABASE_NAME<string>:none
DATABASE_USER<string>:none
DATABASE_PASSWORD<string>:none
DATABASE_HOST<string>:none
DATABASE_PORT<string|int>:none
DATABASE_DRIVER<string>:mysql+mysqlconnector
DATABASE_DIALECT<string>:none
```
You **should** get a result of: 
`{'DATABASE_NAME': None, 'DATABASE_USER': None, 'DATABASE_PASSWORD': None, 'DATABASE_HOST': None, 'DATABASE_PORT': None, 'DATABASE_DRIVER': None, 'DATABASE_DIALECT': None}` This is because the kvProcessor is taking input from the env, and we dont have these env varibles defined. As a result these values default to the defined default value

### Using "Namespaces"
This allows you to "import" kv files from a static host.
```python
from kvprocessor import KVProcessor, KVStructLoader

kv_config_url = "https://github.com/Voxa-Communications/VoxaCommunicaitons-Structures/raw/refs/heads/main/struct/config.json" # STATIC url to json config
kv_struct_loader = KVStructLoader(kv_config_url) # Create a KVStructLoader object with the URL of the config file
kv_processor: KVProcessor = kv_struct_loader.from_namespace("voxa.api.user.user_settings") # Loads the KV file from the URL and returns a KVProcessor object
# For example this loads a file in /api/user/user_settings.kv
user_settings = {
    "2FA_ENABLED": True,
    "TELEMETRY": False,
    "AGE": "25",
    "LANGUAGE": "en",
} # Example Dict Structure
validated_config = kv_processor.process_config(user_settings)
print(validated_config)
```
For an example config.json navigate to `test/config.json`. This file is just what is found on `https://github.com/Voxa-Communications/VoxaCommunicaitons-Structures/blob/main/struct/config.json` which is used in this example.