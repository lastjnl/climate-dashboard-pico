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

# Config
DEVICE_ID = config["device_id"]
API_URL = config["api_url"]

def send_temperature(temperature):
    led_manager.set_led_state('red', False)
    led_manager.set_led_state('orange', True)

    url = API_URL + "room_log"
    postdata = ujson.dumps({ "deviceId": DEVICE_ID, "temperature": str(temperature)})
    response = requests.post(url, json=postdata)

    mqtt.log("Sent temperature data:" + postdata)

    if response.status_code != 200:
        led_manager.set_led_state('red', True)
        responseData = response.json()
        mqtt.log(responseData)
        
    led_manager.set_led_state('orange', False)

def start_measurement_loop(wdt=None):

    # Connect to WiFi
    network_manager.connect(wdt=wdt)

    mqtt.log("start measuring...")
    led_manager.turn_off_all_leds()

    ow_pin = machine.Pin(22)
    ow_bus = onewire.OneWire(ow_pin)
    sensor = ds18x20.DS18X20(ow_bus)

    if wdt:
        wdt.feed()

    devices = sensor.scan()
    if not devices:
        mqtt.log("Geen sensor gevonden!")
    else:
        device_addr = devices[0]
        while True:
            sensor.convert_temp()
            time.sleep_ms(750)
            temp_c = sensor.read_temp(device_addr)
            mqtt.log("Temperatuur: {:.2f} °C".format(temp_c))
            send_temperature(temp_c)

            if wdt:
                wdt.feed()

            mqtt.check_mqtt()
            
            # Sleep in smaller intervals to feed watchdog
            for _ in range(60):  # 60 * 5 = 300 seconds
                time.sleep(5)
                if wdt:
                    wdt.feed()
