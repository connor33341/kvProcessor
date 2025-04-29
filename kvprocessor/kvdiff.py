class KVFileDiffChecker:
    """Compares two .kv files and highlights differences."""
    def __init__(self, file1: str, file2: str):
        self.file1 = file1
        self.file2 = file2

    def diff(self) -> dict:
        with open(self.file1, 'r') as f1, open(self.file2, 'r') as f2:
            lines1 = {line.strip() for line in f1 if line.strip() and not line.startswith('#')}
            lines2 = {line.strip() for line in f2 if line.strip() and not line.startswith('#')}

        added = lines2 - lines1
        removed = lines1 - lines2

        return {
            'added': added,
            'removed': removed
        }