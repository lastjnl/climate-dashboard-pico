import os
import time
from machine import reset_cause, PWRON_RESET, WDT_RESET

print("=" * 50)
print("BOOT SEQUENCE")
print("=" * 50)

# Check reset cause
cause = reset_cause()
print(f"Reset cause: {cause}")

from config import config
import utils.network_manager as network_manager
import utils.mqtt_client as mqtt

# Connect to Network and MQTT early to enable logging
try:
    network_manager.connect()
    mqtt.start_background_listener("device/updates")
    mqtt.log(f"Device {config['device_id']} starting")
except Exception as e:
    print(f"Early network/MQTT init failed: {e}")

# Check for pending updater
if "updater_pending.py" in os.listdir():
    mqtt.log("Applying pending updater update...")
    if "updater.py" in os.listdir():
        os.remove("updater.py")
    os.rename("updater_pending.py", "updater.py")
    mqtt.log("Updater updated successfully")

# Update check with error handling
mqtt.log("Checking for updates...")
try:
    import updater
    update_result = updater.check_for_updates()
    
    if update_result:
        mqtt.log("Update check successful")
    else:
        mqtt.log("Update check returned False, continuing...")
        
except Exception as e:
    mqtt.log(f"Update check failed: {e}")

# Install dependencies
mqtt.log("Checking dependencies...")
try:
    import urequests
    mqtt.log("urequests available")
except ImportError:
    mqtt.log("Installing urequests...")
    import mip
    mip.install('urequests')

mqtt.log("=" * 50)
mqtt.log("Starting main application...")
mqtt.log("=" * 50)

try:
    import app.main as main_app
    main_app.start_measurement_loop()
except KeyboardInterrupt:
    print("\n\nBoot interrupted by user")
    mqtt.log("Device stopped by user")
except Exception as e:
    mqtt.log(f"Main app error: {e}")
    # Fallback mode
    while True:
        time.sleep(5)
        print("Fallback mode...")