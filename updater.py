import network

from config import config

github_main_url = f"https://raw.githubusercontent.com/{config['github_user']}/{config['github_repo']}/main/"
prohibbited_files = ["updater.py", "secrets.py", "config.py"]

def download_manifest():
    print("Downloading manifest...")
    url = f"{github_main_url}manifest.json"
    response = requests.get(url)
    manifest = response.json()
    response.close()
    return manifest

def file_path_exists(file_path):
    try:
        os.stat(file_path)
        return True
    except OSError:
        return False

def mkdir_p(path):
    parts = path.split("/")
    curr = ""
    for part in parts:
        if not part:
            continue
        curr = curr + "/" + part if curr else part
        try:
            os.mkdir(curr)
        except OSError:
            pass

def ensure_directory_exists(file_path):
    if "/" in file_path:
        dir_name = file_path.rsplit("/", 1)[0]
        mkdir_p(dir_name)

def update_file(file_path):
    print(f"Updating file: {file_path}")

    ensure_directory_exists(file_path)

    if file_path_exists(file_path):
        os.remove(file_path)

    url = f"{github_main_url}{file_path}"
    response = requests.get(url)
    with open(file_path, "w") as file:
        file.write(response.text)
    response.close()

# Initalize Wifi, Socket Pool, Request Session
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Connect to Wifi
wlan.connect(config["ssid"], config["password"])
if wlan.isconnected():
    print("Connected to ", config["ssid"])
    print("IP:", wlan.ifconfig()[0])

# Download manifest
manifest = download_manifest()
print("Latest version:", manifest["version"])

# Check against current version, otherwise download and update files
with open(config["version_file"], "r") as version_file:
    current_version = version_file.read().strip()
    if current_version != manifest["version"]:
        print(f"versions do not match, updating to latest version {manifest['version']}")
        for filePath in manifest["files"]:
            print (filePath)
            if filePath not in prohibbited_files:
                update_file(filePath)
            else:
                print(f"Skipping prohibited file: {filePath}")
            