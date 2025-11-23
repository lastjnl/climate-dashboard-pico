from umqtt.simple import MQTTClient
from config import config

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