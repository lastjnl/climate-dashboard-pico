import machine
from config import config
import utils.mqtt_client as mqtt
import utils.network_manager as network_manager
import utils.led_manager as led_manager
import urequests
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
    postdata = { "deviceId": DEVICE_ID, "temperature": str(temperature)}
    
    try:
        response = urequests.post(url, json=postdata)
        mqtt.log("Sent temperature data:" + ujson.dumps(postdata))
        
        if response.status_code != 200:
            led_manager.set_led_state('red', True)
            responseData = response.json()
            mqtt.log(responseData)
        
        response.close()
    except OSError as e:
        led_manager.set_led_state('red', True)
        mqtt.log(f"Network error sending temperature: {e}")
    except Exception as e:
        led_manager.set_led_state('red', True)
        mqtt.log(f"Failed to send temperature: {e}")
        
    led_manager.set_led_state('orange', False)

def start_measurement_loop():

    # Connect to WiFi
    network_manager.connect()

    mqtt.log("start measuring...")
    led_manager.turn_off_all_leds()

    ow_pin = machine.Pin(22)
    ow_bus = onewire.OneWire(ow_pin)
    sensor = ds18x20.DS18X20(ow_bus)

    devices = sensor.scan()
    if not devices:
        mqtt.log("Geen sensor gevonden!")
    else:
        device_addr = devices[0]
        try:
            while True:
                sensor.convert_temp()
                time.sleep_ms(750)
                temp_c = sensor.read_temp(device_addr)
                mqtt.log("Temperatuur: {:.2f} °C".format(temp_c))
                send_temperature(temp_c)

                mqtt.check_mqtt()
                
                # Sleep for 5 minutes
                time.sleep(300)
        except KeyboardInterrupt:
            print("\n\nStopped by user (Ctrl+C)")
            led_manager.turn_off_all_leds()
            print("LEDs turned off. Device ready for new commands.")
