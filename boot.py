import os
import updater
import mip

if "updater_pending.py" in os.listdir():
    if "updater.py" in os.listdir():
        os.remove("updater.py")
        
    os.rename("updater_pending.py", "updater.py")
    os.remove("updater_pending.py")

updater.check_for_updates()

# Install required mip packages
mip.install('urequests')

import app.main