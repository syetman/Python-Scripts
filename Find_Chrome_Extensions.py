# Created: 2024-09-12
# Last Modified: 2024-09-12
# Author: Shaun Yetman
# Description: Search local Windows machine for Chrome extensions
# Returns: str of the extension name and version

import os
import json

# Define the base path to the extensions directory
base_path = os.path.expanduser(r'~\AppData\Local\Google\Chrome\User Data\Default\Extensions')

def check_folder_length(base_path):
    """
    Check for folders in the given path that have a length of 32 characters.

    Args:
    base_path (str): The base directory path to search in.

    Returns:
    list: A list of full paths to folders that have a length of 32 characters.
    """
    return [os.path.join(base_path, folder) for folder in os.listdir(base_path)
            if os.path.isdir(os.path.join(base_path, folder)) and len(folder) == 32]

def get_manifest_file_path(folder_path):
    """
    Find all JSON files in the subfolders of the given folder path.

    Args:
    folder_path (str): The path to the folder to search in.

    Returns:
    list: A list of full paths to JSON files found in the subfolders.
    """
    manifest_paths = []
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        if os.path.isdir(subfolder_path):
            for file in os.listdir(subfolder_path):
                if file.endswith('.json'):
                    manifest_paths.append(os.path.join(subfolder_path, file))
    return manifest_paths

def find_in_json(data, key):
    """
    Recursively search for a key in a JSON-like data structure.

    Args:
    data (dict or list): The JSON-like data structure to search in.
    key (str): The key to search for.

    Returns:
    list: A list of values associated with the given key.
    """
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
