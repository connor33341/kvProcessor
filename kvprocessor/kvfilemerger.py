class KVFileMerger:
    """Merges multiple .kv files into one."""
    def __init__(self, output_path: str):
        self.output_path = output_path

    def merge(self, file_paths: list):
        merged_data = {}
        for file_path in file_paths:
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    key, _, value = line.partition(':')
                    merged_data[key] = value
        with open(self.output_path, 'w') as file:
            for key, value in merged_data.items():
                file.write(f"{key}:{value}\n")