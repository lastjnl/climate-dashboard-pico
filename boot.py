import os

if "update_pending.py" in os.listdir():
    os.remove("updater.py")
    os.rename("update_pending.py", "updater.py")
    os.remove("updater_pending.py")

import updater
#import app.main