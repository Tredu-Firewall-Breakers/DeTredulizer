# Enables Win+R keybind
import winreg
from EasyMenu3 import colors

# Module metadata
NAME = "Enable Win+R"
DESC = "Enables Win+R keybind"

# Variables
PATHS = {
    1: {
        "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer",
        "key": "NoRun"
    },
}

HKEY_LOC = winreg.HKEY_LOCAL_MACHINE

def run():
    reg = winreg.ConnectRegistry(None, HKEY_LOC)
    WINRKey = PATHS[1]

    try:
        with winreg.OpenKey(reg, WINRKey["path"], 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, WINRKey["key"], 0, winreg.REG_DWORD, 0)

        #colors.colored("Signature Check disabled successfully. If you are still restricted, try restarting your computer or executing command again.", colors.OKBLUE)
        print("Win+R keybind activated successfully. This change REQUIRES A RESTART to take effect.")
    except PermissionError:
        colors.fail("Permission denied. Please run this program as an administrator.")
    except Exception as e:
        colors.fail(f"An error occurred: {e}")