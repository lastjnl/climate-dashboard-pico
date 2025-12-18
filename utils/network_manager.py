import utils.led_manager as led_manager
import network


from config import config

def connect():
    led_manager.blink_led('orange', 3, 100)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(config["ssid"], config["password"])
    if wlan.isconnected():
        print("Connected to ", config["ssid"])
        print("IP:", wlan.ifconfig()[0])
        led_manager.set_led_state('green', True)
    else:
        print("Failed to connect to ", config["ssid"])
        led_manager.set_led_state('red', True)