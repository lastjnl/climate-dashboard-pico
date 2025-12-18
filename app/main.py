import machine
from config import config
import utils.mqtt_client as mqtt
import utils.network_manager as network_manager
import utils.led_manager as led_manager
import urequests as requests
import ujson
import onewire
import ds18x20
import time

# Connect to MQTT broker and publish a test message
mqtt.publish("device/updates", f"Device {config['device_id']} is starting up.")
mqtt.listen("device/updates")

# Config
DEVICE_ID = config["device_id"]
API_URL = config["api_url"]

# Connect to WiFi
network_manager.connect()

def send_temperature(temperature):
    led_manager.set_led_state('red', False)
    led_manager.set_led_state('orange', True)

    url = API_URL + "room_log"
    postdata = ujson.dumps({ "deviceId": DEVICE_ID, "temperature": str(temperature)})
    response = requests.post(url, json=postdata)

    if response.status_code != 200:
        led_manager.set_led_state('red', True)
        responseData = response.json()
        print(responseData["status"])
        
    led_manager.set_led_state('orange', False)
            
ow_pin = machine.Pin(22)
ow_bus = onewire.OneWire(ow_pin)
sensor = ds18x20.DS18X20(ow_bus)

devices = sensor.scan()
if not devices:
    print("Geen sensor gevonden!")
else:
    device_addr = devices[0]
    while True:
        sensor.convert_temp()
        time.sleep_ms(750)
        temp_c = sensor.read_temp(device_addr)
        print("Temperatuur: {:.2f} °C".format(temp_c))
        send_temperature(temp_c)
        time.sleep(300)
