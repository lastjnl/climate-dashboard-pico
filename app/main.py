from config import config
import utils.mqtt_client as mqtt

# Connect to MQTT broker and publish a test message
mqtt.publish("device/updates", f"Device {config['device_id']} is starting up.")
mqtt.listen("device/updates")

# import os

# import time
# import board
# import adafruit_onewire.bus
# import adafruit_ds18x20
# import wifi
# import socketpool
# import adafruit_requests
# import json
# import adafruit_connection_manager

# from digitalio import *
# from secrets import secrets

# # Config
# DEVICE_ID = secrets["device_id"]
# API_URL = secrets["api_url"]
# SSID = secrets["ssid"]

# # Leds
# led_green = DigitalInOut(board.GP0)
# led_green.direction = Direction.OUTPUT
# led_orange = DigitalInOut(board.GP1)
# led_orange.direction = Direction.OUTPUT
# led_red = DigitalInOut(board.GP2)
# led_red.direction = Direction.OUTPUT

# # Initalize Wifi, Socket Pool, Request Session
# pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
# ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
# requests = adafruit_requests.Session(pool, ssl_context)

# networks = wifi.radio.start_scanning_networks()
# network_found = False
# for network in networks:
#     if (network.ssid == SSID and network_found == False):
#         print(f"Found network {network.ssid}")
#         print(f"Network Strenght: {network.rssi}")
#         network_found = True

# print(f"Connect to {SSID}...")
# try:
#     wifi.radio.connect(secrets["ssid"], secrets["password"])
# except:
#     print("Cannot connect to:", secrets["ssid"])
#     led_red.value = True
    
# if wifi.radio.connected:
#     led_green.value = True
#     print("Connected to ", secrets["ssid"])
#     print("IP:", wifi.radio.ipv4_address)

# def send_temperature(temperature):
#     led_red.value = False
#     led_orange.value = True
#     url = API_URL + "room_log"
#     postdata = {
#         "deviceId": DEVICE_ID,
#         "temperature": str(temperature)
#     }
#     jsonPostData=json.dumps(postdata)
#     with requests.post(url, data=jsonPostData) as response:
#         if response.status_code != 200:
#             led_red.value = True
#             responseData = response.json()
#             print(responseData["status"])
#         led_orange.value = False
            
# # Kies de pin waar je DS18B20 op hebt aangesloten
# ow_pin = board.GP22  # gebruik jouw pin hier
# ow_bus = adafruit_onewire.bus.OneWireBus(ow_pin)
# devices = ow_bus.scan()

# if not devices:
#     print("Geen sensor gevonden!")
# else:
#     # Gebruik de eerste sensor
#     ds18 = adafruit_ds18x20.DS18X20(ow_bus, devices[0])

#     while wifi.radio.connected:
#         temp_c = ds18.temperature
#         print("Temperatuur: {:.2f} °C".format(temp_c))
#         send_temperature(temp_c)
#         time.sleep(10)
