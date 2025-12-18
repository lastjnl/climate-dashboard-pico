import os
import updater
import mip
import app.main as main_app
import utils.mqtt_client as mqtt

from config import config

if "updater_pending.py" in os.listdir():
    if "updater.py" in os.listdir():
        os.remove("updater.py")
        
    os.rename("updater_pending.py", "updater.py")
    os.remove("updater_pending.py")

updater.check_for_updates()

# Install required mip packages
mip.install('urequests')

# Connect to MQTT broker and publish a test message
print("Connecting to MQTT broker...")
mqtt.publish("device/updates", f"Device {config['device_id']} is starting up.")
mqtt.listen("device/updates")

print("Starting main application...")
main_app.start_measurement_loop()
