import hashlib
import os
import json

HASH_FILE = "file_hashes.json"

def calculate_hash(file_path, algorithm='sha256'):
    hasher = hashlib.new(algorithm)
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None

def load_hashes():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_hashes(hashes):
    with open(HASH_FILE, 'w') as f:
        json.dump(hashes, f, indent=4)

def monitor_files(file_paths):
    stored_hashes = load_hashes()
    current_hashes = {}
    
    for file in file_paths:
        file_hash = calculate_hash(file)
        if file_hash:
            current_hashes[file] = file_hash
            if file in stored_hashes:
                if stored_hashes[file] != file_hash:
                    print(f"WARNING: {file} has been modified!")
                else:
                    print(f"{file} is unchanged.")
            else:
                print(f"New file detected: {file}")
    
    save_hashes(current_hashes)
    print("Hash records updated.")

if __name__ == "__main__":
    files_to_monitor = ["example.txt", "test.docx"]  # Add files to monitor here
    monitor_files(files_to_monitor)


#output
