# Gives user a small menu to configure Windows Update regedit parameters
import winreg
from datetime import datetime

from EasyMenu3 import colors

# Module metadata
NAME = "Configure Windows Updates"
DESC = "Configuration menu to change different Windows Update parameters."

# Variables
PATHS = {
    1: { # Allow changing the pause updates button in Settings > Windows Update
        "path": r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate",
        "key": "SetDisablePauseUXAccess"
    },
    2: { # How many days to pause settings for
        "path": r"SOFTWARE\Microsoft\Windows\WindowsUpdate\UX\Settings",
        "key": "FlightSettingsMaxPauseDays"
    },
    3: {
        "path": r"SOFTWARE\Microsoft\Windows\WindowsUpdate\UX\Settings",
        "key": "PauseFeatureUpdatesStartTime"
    },
    4: {
        "path": r"SOFTWARE\Microsoft\Windows\WindowsUpdate\UX\Settings",
        "key": "PauseFeatureUpdatesEndTime"
    },
    5: {
        "path": r"SOFTWARE\Microsoft\Windows\WindowsUpdate\UX\Settings",
        "key": "PauseQualityUpdatesStartTime"
    },
    6: {
        "path": r"SOFTWARE\Microsoft\Windows\WindowsUpdate\UX\Settings",
        "key": "PauseQualityUpdatesEndTime"
    },
    7: {
        "path": r"SOFTWARE\Microsoft\Windows\WindowsUpdate\UX\Settings",
        "key": "PauseUpdatesStartTime"
    },
    8: {
        "path": r"SOFTWARE\Microsoft\Windows\WindowsUpdate\UX\Settings",
        "key": "PauseUpdatesExpiryTime"
    }
}

HKEY_LOC = winreg.HKEY_LOCAL_MACHINE

PAUSE_DAYS_DEFAULT = 7300

def run():
    reg = winreg.ConnectRegistry(None, HKEY_LOC)
    PauseUpdatesButtonKey = PATHS[1]
    PauseDaysKey = PATHS[2]
    DatetimeStartKeys = [PATHS[3], PATHS[5], PATHS[7]]
    DatetimeEndKeys = [PATHS[4], PATHS[6], PATHS[8]]

    try:
        # Enable access to Pause Updates button
        with winreg.OpenKey(reg, PauseUpdatesButtonKey["path"], 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, PauseUpdatesButtonKey["key"], 0, winreg.REG_DWORD, 0)

        with winreg.OpenKey(reg, PauseDaysKey["path"], 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, PauseDaysKey["key"], 0, winreg.REG_DWORD, PAUSE_DAYS_DEFAULT)

        print("Access to Pause Updates button enabled...")
        pause_till_year = input("Enter Pause Update Year (Default: Current Year + 10, Q to exit plugin): ")

        if pause_till_year.lower() == "q":
            print("Plugin exited")
            return
        elif not pause_till_year:
            pause_till_year = datetime.now().year + 10
        elif int(pause_till_year) < int(datetime.now().year):
            print("Invalid Year")
            return

        # Set Pause Update related keys
        print(f"Setting Pause Update expiry time to {pause_till_year}...")

        for key_info in DatetimeEndKeys:
            # Edit keys into YYYY-MM-DDTHH:MM:SS format, with time set to 00:00:00
            pause_time_str = f"{pause_till_year}-12-31T00:00:00"
            pause_time = int(datetime.strptime(pause_time_str, "%Y-%m-%dT%H:%M:%S").timestamp())

            with winreg.OpenKey(reg, key_info["path"], 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, key_info["key"], 0, winreg.REG_SZ, pause_time)

        for key_info in DatetimeStartKeys:
            # Set start time to current time
            current_time = int(datetime.now().timestamp())

            with winreg.OpenKey(reg, key_info["path"], 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, key_info["key"], 0, winreg.REG_SZ, current_time)

        #colors.colored("Signature Check disabled successfully. If you are still restricted, try restarting your computer or executing command again.", colors.OKBLUE)
        print("Settings applied successfully.")
    except PermissionError:
        colors.fail("Permission denied. Please run this program as an administrator.")
    except Exception as e:
        colors.fail(f"An error occurred: {e}")