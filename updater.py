import os
import time
import wifi
import socketpool
import adafruit_requests
import json
import adafruit_connection_manager

from config import config

def download_manifest():
    print("Downloading manifest...")
    url = f"https://raw.githubusercontent.com/{config['github_user']}/{config['github_repo']}/main/manifest.json"
    response = requests.get(url)
    manifest = response.json()
    response.close()
    return manifest

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

# Connect to Wifi
wifi.radio.connect(config["ssid"], config["password"])
if wifi.radio.connected:
    print("Connected to ", config["ssid"])
    print("IP:", wifi.radio.ipv4_address)

# Download manifest
manifest = download_manifest()
print("Latest version:", manifest["version"])