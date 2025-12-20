import utils.led_manager as led_manager
import network
import time


from config import config

def connect(wdt=None, timeout_s=15):
    led_manager.set_led_state('green', False)
    led_manager.set_led_state('red', False)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        print("Already connected to ", config["ssid"])
        print("IP:", wlan.ifconfig()[0])
        led_manager.set_led_state('green', True)
        return
    
    print("Connecting with wifi...")

    wlan.connect(config["ssid"], config["password"])

    start = time.time()
    while not wlan.isconnected():
        if wdt:
            wdt.feed()

        if time.time() - start > timeout_s:
            print("Connection timed out")
            led_manager.set_led_state('red', True)
            return False
        time.sleep(1)

        time.sleep(0.5)

    print("Connected to ", config["ssid"])
    print("IP:", wlan.ifconfig()[0])
    led_manager.set_led_state('green', True)