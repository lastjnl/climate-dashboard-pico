import machine
import updater

def handle_incomming_message(topic, msg):
    import utils.mqtt_client as mqtt

    if "new update available" in msg.decode():
        mqtt.log("Update message received, starting update process...")
        updater.check_for_updates(force=True)
    else:
        mqtt.log(f"Received message on topic {topic.decode()}: {msg.decode()}")