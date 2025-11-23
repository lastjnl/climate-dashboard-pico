import network

from config import config

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(config["ssid"], config["password"])
    if wlan.isconnected():
        print("Connected to ", config["ssid"])
        print("IP:", wlan.ifconfig()[0])