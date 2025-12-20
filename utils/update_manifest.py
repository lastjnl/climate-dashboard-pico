import os
import json

print("Updating Manifest...")

# Get current manifest content
with open("manifest.json", "r") as f:
    content = json.decoder.JSONDecoder().decode(f.read())

current_version = content.get("version", "0.0.0")
print(f"Current version: {current_version}")

# Bump version number
major, minor, patch = map(int, current_version.split("."))
patch += 1
new_version = f"{major}.{minor}.{patch}"
content["version"] = new_version
print(f"New version: {new_version}")

# read all files 
files_folders_to_skip = {".git", ".vscode", "__pycache__"}

def getFileListFromDir(directory="."):
    application_files = dict()
    
    for file_name in os.listdir(directory):
        if file_name in files_folders_to_skip:
            continue
        
        full_path = os.path.join(directory, file_name)
        
        if os.path.isdir(full_path):
            # Recursively get files from subdirectory
            directory_files = getFileListFromDir(full_path)
            for sub_file, sub_path in directory_files.items():
                application_files[sub_path] = sub_path.replace("./", "")
        else:
            # Add the file with its relative path
            application_files[file_name] = full_path.replace("./", "")
    
    return application_files

# Get all files
content["files"] = getFileListFromDir()

# Write updated manifest back to file not in a single line
with open("manifest.json", "w") as f:
    f.write(json.dumps(content, indent=4))
