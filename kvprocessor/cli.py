import argparse
from kvprocessor.kvvalidator import validate_kv_file
from kvprocessor.kvmanifestloader import KVManifestLoader
from kvprocessor.kvnamespacemanager import NamespaceManager
from kvprocessor.kvprocessor import KVProcessor
from kvprocessor.kvglobalsettings import get_version

def main():
    parser = argparse.ArgumentParser(description="CLI for kvProcessor")
    parser.add_argument("--version", action="version", version=f"kvProcessor {get_version()}", help="Show the version of kvProcessor")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: Validate .kv file
    validate_parser = subparsers.add_parser("validate", help="Validate a .kv file")
    validate_parser.add_argument("file", type=str, help="Path to the .kv file")

    # Subcommand: List namespaces
    list_parser = subparsers.add_parser("list-namespaces", help="List all namespaces")
    list_parser.add_argument("manifest", type=str, help="Path to the manifest file")

    # Subcommand: Validate manifest
    validate_manifest_parser = subparsers.add_parser("validate-manifest", help="Validate a manifest file")
    validate_manifest_parser.add_argument("manifest", type=str, help="Path to the manifest file")

    # Subcommand: Add namespace
    add_parser = subparsers.add_parser("add-namespace", help="Add a new namespace")
    add_parser.add_argument("manifest", type=str, help="Path to the manifest file")
    add_parser.add_argument("key", type=str, help="Namespace key")
    add_parser.add_argument("value", type=str, help="Namespace value")

    # Subcommand: Remove namespace
    remove_parser = subparsers.add_parser("remove-namespace", help="Remove a namespace")
    remove_parser.add_argument("manifest", type=str, help="Path to the manifest file")
    remove_parser.add_argument("key", type=str, help="Namespace key")

    # Subcommand: Export configuration
    export_parser = subparsers.add_parser("export-config", help="Export configuration to a .kv file")
    export_parser.add_argument("config", type=str, help="Path to the configuration JSON file")
    export_parser.add_argument("output", type=str, help="Path to the output .kv file")

    # Subcommand: Merge .kv files
    merge_parser = subparsers.add_parser("merge-kv", help="Merge multiple .kv files into one")
    merge_parser.add_argument("files", nargs='+', help="Paths to the .kv files to merge")
    merge_parser.add_argument("output", type=str, help="Path to the output .kv file")

    args = parser.parse_args()

    if args.command == "validate":
        try:
            if validate_kv_file(args.file):
                print(f"{args.file} is valid.")
        except Exception as e:
            print(f"Validation failed: {e}")

    elif args.command == "list-namespaces":
        try:
            manifest_loader = KVManifestLoader(args.manifest)
            manager = NamespaceManager(manifest_loader)
            namespaces = manager.list_namespaces()
            print("Available namespaces:")
            for namespace in namespaces:
                print(namespace)
        except Exception as e:
            print(f"Error listing namespaces: {e}")

    elif args.command == "validate-manifest":
        try:
            manifest_loader = KVManifestLoader(args.manifest)
            manifest_loader.validate_manifest()
            print(f"Manifest {args.manifest} is valid.")
        except Exception as e:
            print(f"Manifest validation failed: {e}")

    elif args.command == "add-namespace":
        try:
            manifest_loader = KVManifestLoader(args.manifest)
            manager = NamespaceManager(manifest_loader)
            manager.add_namespace(args.key, args.value)
            print(f"Namespace {args.key} added successfully.")
        except Exception as e:
            print(f"Error adding namespace: {e}")

    elif args.command == "remove-namespace":
        try:
            manifest_loader = KVManifestLoader(args.manifest)
            manager = NamespaceManager(manifest_loader)
            manager.remove_namespace(args.key)
            print(f"Namespace {args.key} removed successfully.")
        except Exception as e:
            print(f"Error removing namespace: {e}")

    elif args.command == "export-config":
        from kvprocessor.kvfileexporter import KVFileExporter
        import json
        try:
            with open(args.config, 'r') as config_file:
                config = json.load(config_file)
            exporter = KVFileExporter(args.output)
            exporter.validate_and_export(config)
            print(f"Configuration exported to {args.output}.")
        except Exception as e:
            print(f"Error exporting configuration: {e}")

    elif args.command == "merge-kv":
        from kvprocessor.kvfilemerger import KVFileMerger
        try:
            merger = KVFileMerger(args.output)
            merger.merge(args.files)
            print(f"Merged .kv files into {args.output}.")
        except Exception as e:
            print(f"Error merging .kv files: {e}")

if __name__ == "__main__":
    main()