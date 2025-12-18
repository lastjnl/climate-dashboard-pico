import machine

# Leds
led_green = machine.Pin(0, machine.Pin.OUT)
led_orange = machine.Pin(1, machine.Pin.OUT)
led_red = machine.Pin(2, machine.Pin.OUT)

led_map = {
    'green': led_green,
    'orange': led_orange,
    'red': led_red
}

def blink_led(led_name, times, delay=200):
    led = led_map.get(led_name.lower())
    check_if_led_exists(led)
    
    for _ in range(times):
        led.on()
        machine.sleep(delay)
        led.off()
        machine.sleep(delay)

def set_led_state(led_name, state):
    led = led_map.get(led_name.lower())
    check_if_led_exists(led)
    
    if state:
        led.on()
    else:
        led.off()

def check_if_led_exists(led):
    if led is None:
        raise ValueError(f"Unknown LED - Choose from: {list(led_map.keys())}")
    return True

def turn_off_all_leds():
    for led in led_map.values():
        led.off()