import os
import network
import urequests as requests
import machine
import time

from utils import network_manager
from config import config

import mqtt_client

github_main_url = f"https://raw.githubusercontent.com/{config['github_user']}/{config['github_repo']}/main/"
prohibbited_files = ["updater.py", "config.py"]

def download_manifest():
    print("Downloading manifest...")
    url = f"{github_main_url}manifest.json?nocache={time.time()}"
    response = requests.get(url=url)
    manifest = response.json()
    response.close()
    return manifest

def ensure_directory_exists(file_path):
    if "/" in file_path:
        dir_name = file_path.rsplit("/", 1)[0]
        try:
            os.stat(dir_name)
        except OSError:
            parts = dir_name.split("/")
            current = ""
            for part in parts:
                if not part:
                    continue
                current = current + "/" + part if current else part
                try:
                    os.stat(current)
                except OSError:
                    os.mkdir(current)
    else:
        return True
    
def file_path_exists(file_path):
    try:
        os.stat(file_path)
        return True
    except OSError:
        return False

def update_file(file_path, tmp_file_path=None):
    print(f"Updating file: {file_path}")

    ensure_directory_exists(file_path)

    if file_path_exists(file_path) and not tmp_file_path:
        os.remove(file_path)
        
    url = f"{github_main_url}{file_path}"
    response = requests.get(url=url)
    if tmp_file_path:
        file_path = tmp_file_path
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
            if filePath == "updater.py":
                print("updating updater.py via tmp file...")
                tmp_filePath = "updater_pending.py"
                update_file(filePath, tmp_filePath)
            elif filePath not in prohibbited_files:
                update_file(filePath)
            else:
                print(f"Skipping prohibited file: {filePath}")

        with open(config["version_file"], "w") as version_file:
            version_file.write(manifest["version"])

        mqtt_client.publish("device/updates", f"Device {config['device_id']} updated to version {manifest['version']}")
        print("Update complete, restarting...")
        machine.reset()
    else:
        print("Already at latest version.")
            