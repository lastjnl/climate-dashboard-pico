import os
import time
from machine import reset_cause, PWRON_RESET, WDT_RESET, WDT

print("=" * 50)
print("BOOT SEQUENCE")
print("=" * 50)

# Check reset cause
cause = reset_cause()
print(f"Reset cause: {cause}")
# PWRON_RESET = 1 (power on or hard reset)
# WDT_RESET = 3 (watchdog reset)

# Boot loop detection
RESET_COUNTER_FILE = "reset_count.txt"
MAX_RESETS = 3

def get_reset_count():
    try:
        with open(RESET_COUNTER_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 0

def increment_reset_count():
    count = get_reset_count() + 1
    with open(RESET_COUNTER_FILE, "w") as f:
        f.write(str(count))
    return count

def clear_reset_count():
    try:
        os.remove(RESET_COUNTER_FILE)
    except:
        pass

# Check if this was a watchdog reset
if cause == WDT_RESET:
    reset_count = increment_reset_count()
    print(f"⚠️  Watchdog reset detected! Count: {reset_count}/{MAX_RESETS}")
    
    if reset_count >= MAX_RESETS:
        print("=" * 50)
        print("🛑 SAFE MODE ACTIVATED")
        print("Too many watchdog resets detected!")
        print("Skipping auto-update to prevent boot loop")
        print("=" * 50)
        
        # Create safe mode flag
        with open("safe_mode.txt", "w") as f:
            f.write(f"Activated after {reset_count} watchdog resets")
        
        # Clear counter for next time
        clear_reset_count()
        
        # Enter safe mode - skip updates, run minimal code
        SAFE_MODE = True
    else:
        print(f"Attempting boot... ({reset_count}/{MAX_RESETS} attempts)")
        SAFE_MODE = False
else:
    # Normal power-on, clear the counter
    print("Normal boot (power on or manual reset)")
    clear_reset_count()
    SAFE_MODE = False

# Check for existing safe mode file
if "safe_mode.txt" in os.listdir():
    print("⚠️  Safe mode file detected")
    SAFE_MODE = True

# Now continue with boot based on mode
if SAFE_MODE:
    print("=" * 50)
    print("RUNNING IN SAFE MODE")
    print("To exit safe mode: delete 'safe_mode.txt' and reset")
    print("=" * 50)
    
    # Minimal boot - no updates, no watchdog
    try:
        from config import config
        print(f"Device ID: {config.get('device_id', 'unknown')}")
        print("Main application starting in safe mode...")
        
        import app.main as main_app
        main_app.start_measurement_loop()  # No watchdog
        
    except Exception as e:
        print(f"Even safe mode failed: {e}")
        # Just keep device alive
        while True:
            time.sleep(60)
            print("Safe mode - waiting...")
    
else:
    # Normal boot with watchdog and updates
    print("=" * 50)
    print("NORMAL BOOT MODE")
    print("=" * 50)
    
    from config import config
    
    # Initialize watchdog
    print("Initializing watchdog (8 seconds)...")
    wdt = WDT(timeout=8000)
    wdt.feed()
    
    # Check for pending updater
    if "updater_pending.py" in os.listdir():
        print("Applying pending updater update...")
        if "updater.py" in os.listdir():
            os.remove("updater.py")
        os.rename("updater_pending.py", "updater.py")
        print("Updater updated successfully")
    
    wdt.feed()
    
    # Update check with error handling
    print("Checking for updates...")
    try:
        import updater
        wdt.feed()
        
        update_result = updater.check_for_updates(wdt)
        wdt.feed()
        
        if update_result:
            print("Update check successful")
            # Clear reset counter on successful update
            clear_reset_count()
        else:
            print("Update check returned False, continuing...")
            
    except Exception as e:
        print(f"Update check failed: {e}")
        wdt.feed()
    
    wdt.feed()
    
    # Install dependencies
    print("Checking dependencies...")
    try:
        import urequests
        print("✓ urequests available")
    except ImportError:
        print("Installing urequests...")
        import mip
        wdt.feed()
        mip.install('urequests')
        wdt.feed()
    
    wdt.feed()
    
    # Connect to MQTT
    print("Connecting to MQTT broker...")
    try:
        import utils.mqtt_client as mqtt
        wdt.feed()
        mqtt.publish("device/updates", f"Device {config['device_id']} starting")
        wdt.feed()
        mqtt.start_background_listener("device/updates")
        wdt.feed()
    except Exception as e:
        print(f"MQTT error: {e}")
        wdt.feed()
    
    print("=" * 50)
    print("Starting main application...")
    print("=" * 50)
    wdt.feed()
    
    # Clear reset counter on successful boot
    clear_reset_count()
    
    try:
        import app.main as main_app
        wdt.feed()
        main_app.start_measurement_loop(wdt)
    except Exception as e:
        print(f"Main app error: {e}")
        wdt.feed()
        # Fallback mode
        while True:
            wdt.feed()
            time.sleep(5)
            print("Fallback mode...")