from kvprocessor import LoadEnv, KVProcessor

if __name__ == "__main__":
    kv_file_path = "test/test.kv" # Directory to .kv file
    kv_processor = KVProcessor(kv_file_path) # Create a KV processor class
    kv_keys = kv_processor.return_names() # Gets the keys (VARIBLENAME) from the .kv file
    env_list = LoadEnv(kv_keys) # Loads all the ENV varibles that match those keys
    validated_config = kv_processor.process_config(env_list) # Verifies that those env varibles exist and are of the correct type
    print(validated_config)