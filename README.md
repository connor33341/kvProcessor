# kvProcessor

[**PYPI Package**](https://pypi.org/project/kvprocessor/) \
[**GitHub**](https://github.com/connor33341/kvProcessor) \
A Python package for processing and validating configuration dictionaries against a custom `.kv` file format.

## Installation

Install via pip:

```bash
pip install kvprocessor
```

## File format

```custom
# Comments are defined by a "#"
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

### Namespace's config.json
Namespace JSON files, have to be on a static host. They cannot be used locally. The easiest way to do this is to make a github repo, and use the raw file.
#### A config.json in a namespace should include at least two parts:
 - A "root", the name that preceedes the rest of the namespace. Ex: `voxa` in `voxa.api.user.user_settings`
 - A "URL". Ex: `https://mysite.example/kvstructures`, when the namespace `mysite.folder.structure` is used (assuming `root` is set to `mysite`), will fetch `https://mysite.example/kvstructures/folder/structure.kv`

 Here is an example JSON (Note: on 0.7.1+ the URL is not needed, however a `struct` needs to be defined):
```json
{
    "root": "voxa",
    "version": "0.1.5",
    "URL": "https://raw.githubusercontent.com/Voxa-Communications/VoxaCommunicaitons-Structures/refs/heads/main/struct/"
}
```

## Building
For building the library locally \
**Requires**: `python3.8+`, `pip`, `linux system`(if using the predefined shell files)

 1. `git clone https://github.com/connor33341/kvProcessor.git`
 2. `cd kvProcessor`
 3. `bash build.sh`

`build.sh` will also install kvProcessor as a local package, which you will be able to use.
If you add new features to your fork, and would like them to be featured on the main repo. Submit a Pull Request
## For the nerds
The syntax was already mentioned, however if you would like to see how it parses. The following regex is used to determine the: `name`, `type`, and `default`:
```re
(\w+)<([\w\|]+)>:([\w+]+|none)
```
With this knowlege, you probably can figure out a way to write .kv files in a weird way. Out of typical standard.