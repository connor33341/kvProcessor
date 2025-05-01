from kvprocessor import KVProcessor, KVStructLoader
import json
import sys

def display_menu():
    print("\nMenu:")
    print("1. Load Namespace")
    print("2. Process Data")
    print("3. Export Data")
    print("4. Exit")

def load_namespace(kv_struct_loader):
    namespace = input("Enter Namespace: ")
    try:
        kv_processor = kv_struct_loader.from_namespace(namespace)
        print(f"Namespace '{namespace}' loaded successfully.")
        return kv_processor
    except Exception as e:
        print(f"Error loading namespace: {e}")
        return None

def process_data(kv_processor):
    if not kv_processor:
        print("No namespace loaded. Please load a namespace first.")
        return
    try:
        data = input("Enter data to process (JSON format): ")
        parsed_data = json.loads(data)
        processed_data = kv_processor.process(parsed_data)
        print("Processed Data:")
        print(json.dumps(processed_data, indent=4))
    except Exception as e:
        print(f"Error processing data: {e}")

def export_data(kv_processor):
    if not kv_processor:
        print("No namespace loaded. Please load a namespace first.")
        return
    try:
        export_path = input("Enter export file path: ")
        kv_processor.export(export_path)
        print(f"Data exported successfully to {export_path}.")
    except Exception as e:
        print(f"Error exporting data: {e}")

if __name__ == "__main__":
    print("KV Processor Initialized")
    kv_struct_loader = KVStructLoader("https://github.com/Voxa-Communications/VoxaCommunicaitons-Structures/raw/refs/heads/main/struct/config.json")
    kv_processor = None

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            kv_processor = load_namespace(kv_struct_loader)
        elif choice == "2":
            process_data(kv_processor)
        elif choice == "3":
            export_data(kv_processor)
        elif choice == "4":
            print("Exiting KV Processor.")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")