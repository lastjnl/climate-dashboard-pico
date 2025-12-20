from umqtt.robust import MQTTClient 
from config import config
import time

from utils.mqtt_message_handler import handle_incomming_message as callback

_active_client = None

def connect():
    try:
        client = MQTTClient(
            client_id=config["device_id"],
            server=config["mqtt_broker"],
            user=config["mqtt_user"],
            password=config["mqtt_password"]
        )
        client.connect(clean_session=True)
        return client
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        return None

def publish(topic, message):
    client = connect()
    if client:
        client.publish(topic, message)
        client.disconnect()

def start_background_listener(topic):
    global _active_client
    _active_client = connect()
    if _active_client:
        _active_client.set_callback(callback)
        _active_client.subscribe(topic)
        print("MQTT client is now listening in the background to topic:", topic)

def log(message):
    print(message)
    global _active_client
    # Use existing connection if available, otherwise try to connect
    if not _active_client:
        _active_client = connect()
    
    if _active_client:
        device_message = f"Device {config['device_id']}: {message}"
        try:
            _active_client.publish("device/information", str(device_message))
        except Exception as e:
            print(f"Failed to log to MQTT: {e}")
            _active_client = None

def check_mqtt():  # Call this periodically from your main loop
    global _active_client
    if _active_client:
        try:
            _active_client.check_msg()  # Non-blocking if socket set properly
        except Exception as e:
            print("MQTT check error:", e)
            # Optionally reconnect
            _active_client = None
            start_background_listener("device/updates")  # pass topic or store it