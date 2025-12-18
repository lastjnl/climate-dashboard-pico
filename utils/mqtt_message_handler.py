import machine

def handle_incomming_message(topic, msg):

    if "new update available" in msg.decode():
        print("Update message received, restarting to apply update...")
        machine.reset()
    else:
        print(f"Received message on topic {topic.decode()}: {msg.decode()}")