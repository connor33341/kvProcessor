class KVFileExporter:
    """Exports processed configuration back into a .kv file format."""
    def __init__(self, output_path: str):
        self.output_path = output_path

    def export(self, config: dict):
        """Exports the configuration dictionary to a .kv file."""
        try:
            with open(self.output_path, 'w') as file:
                for key, value in config.items():
                    value_type = type(value).__name__
                    if value is None:
                        value = 'none'
                    file.write(f"{key}<{value_type}>:{value}\n")
        except IOError as e:
            raise IOError(f"Failed to write to file {self.output_path}: {e}")

    def validate_and_export(self, config: dict):
        """Validates the configuration dictionary before exporting."""
        if not isinstance(config, dict):
            raise TypeError("Configuration must be a dictionary.")

        for key, value in config.items():
            if not isinstance(key, str):
                raise ValueError(f"Invalid key type: {key}. Keys must be strings.")

        self.export(config)

    def append_to_file(self, additional_config: dict):
        """Appends additional configuration to the existing .kv file."""
        try:
            with open(self.output_path, 'a') as file:
                for key, value in additional_config.items():
                    value_type = type(value).__name__
                    if value is None:
                        value = 'none'
                    file.write(f"{key}<{value_type}>:{value}\n")
        except IOError as e:
            raise IOError(f"Failed to append to file {self.output_path}: {e}")