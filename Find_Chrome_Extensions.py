import os
import json

# Define the base path to the extensions directory
base_path = os.path.expanduser(r'~\AppData\Local\Google\Chrome\User Data\Default\Extensions')

def check_folder_length(base_path):
    return [os.path.join(base_path, folder) for folder in os.listdir(base_path)
            if os.path.isdir(os.path.join(base_path, folder)) and len(folder) == 32]

def get_manifest_file_path(folder_path):
    manifest_paths = []
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        if os.path.isdir(subfolder_path):
            for file in os.listdir(subfolder_path):
                if file.endswith('.json'):
                    manifest_paths.append(os.path.join(subfolder_path, file))
    return manifest_paths

def find_in_json(data, key):
    results = []
    
    def recursive_search(item):
        if isinstance(item, dict):
            for k, v in item.items():
                if k == key:
                    results.append(v)
                elif isinstance(v, (dict, list)):
                    recursive_search(v)
        elif isinstance(item, list):
            for element in item:
                recursive_search(element)
    
    recursive_search(data)
    return results

def get_extensions_info():
    extensions_info = []
    
    folders = check_folder_length(base_path)
    for folder in folders:
        manifest_paths = get_manifest_file_path(folder)
        for manifest_path in manifest_paths:
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest_data = json.load(f)
                
                names = find_in_json(manifest_data, "name")
                versions = find_in_json(manifest_data, "version")
                
                if names and versions:
                    extensions_info.append((names[0], versions[0]))
            except Exception as e:
                print(f"Error processing {manifest_path}: {str(e)}")
    
    return extensions_info

# Run the function and print the results
if __name__ == "__main__":
    extensions = get_extensions_info()
    for name, version in extensions:
        print(f"Extension: {name}, Version: {version}")
