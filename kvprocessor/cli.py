import argparse
from kvprocessor.kvvalidator import validate_kv_file
from kvprocessor.kvmanifestloader import KVManifestLoader, NamespaceManager
from kvprocessor.kvprocessor import KVProcessor

def main():
    parser = argparse.ArgumentParser(description="CLI for kvProcessor")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: Validate .kv file
    validate_parser = subparsers.add_parser("validate", help="Validate a .kv file")
    validate_parser.add_argument("file", type=str, help="Path to the .kv file")

    # Subcommand: List namespaces
    list_parser = subparsers.add_parser("list-namespaces", help="List all namespaces")
    list_parser.add_argument("manifest", type=str, help="Path to the manifest file")

    # Subcommand: Add namespace
    add_parser = subparsers.add_parser("add-namespace", help="Add a new namespace")
    add_parser.add_argument("manifest", type=str, help="Path to the manifest file")
    add_parser.add_argument("key", type=str, help="Namespace key")
    add_parser.add_argument("value", type=str, help="Namespace value")

    # Subcommand: Remove namespace
    remove_parser = subparsers.add_parser("remove-namespace", help="Remove a namespace")
    remove_parser.add_argument("manifest", type=str, help="Path to the manifest file")
    remove_parser.add_argument("key", type=str, help="Namespace key")

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

if __name__ == "__main__":
    main()