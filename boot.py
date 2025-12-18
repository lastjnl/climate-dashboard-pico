import os

if "updater_pending.py" in os.listdir():
    if "updater.py" in os.listdir():
        os.remove("updater.py")
        
    os.rename("updater_pending.py", "updater.py")
    os.remove("updater_pending.py")

import updater
import app.main