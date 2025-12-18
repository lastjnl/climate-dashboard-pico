from umqtt.robust import MQTTClient 
from config import config
import time

from utils.mqtt_message_handler import handle_incomming_message as callback

def connect():
    try:
        client = MQTTClient(
            client_id=config["device_id"],
            server=config["mqtt_broker"],
            user=config["mqtt_user"],
            password=config["mqtt_password"]
        )
        client.connect()
        return client
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        return None

def publish(topic, message):
    client = connect()
    if client:
        client.publish(topic, message)
        client.disconnect()

def listen(topic):
    client = connect()
    if client:
        client.set_callback(callback)
        client.subscribe(topic)

        try:
            while True:
                client.check_msg()
                time.sleep(1)
        finally:
            client.disconnect()