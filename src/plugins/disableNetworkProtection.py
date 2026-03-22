# Disables Windows Defender Network Protection
import winreg
from EasyMenu3 import colors

# Module metadata
NAME = "Disable Network Protection"
DESC = "Disables Windows Defender Network Protection, allowing usage of certain web pages and web apps, including Steam."

# Variables
PATHS = {
    1: { # Defender key
        "path": r"SOFTWARE\Policies\Microsoft\Windows Defender\Policy Manager",
        "key": "EnableNetworkProtection"
    },
    2: { # Intune key
        "path": r"SOFTWARE\Microsoft\PolicyManager\current\device\Defender",
        "key": "EnableNetworkProtection_WinningProvider"
    }
}

HKEY_LOC = winreg.HKEY_LOCAL_MACHINE

def run():
    reg = winreg.ConnectRegistry(None, HKEY_LOC)
    defender_key = PATHS[1]
    intune_key = PATHS[2]

    try:
        # Disable Defender Network Protection
        with winreg.OpenKey(reg, defender_key["path"], 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, defender_key["key"], 0, winreg.REG_DWORD, 0)

        # Disable Intune Network Protection
        with winreg.OpenKey(reg, intune_key["path"], 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, intune_key["key"], 0, winreg.REG_DWORD, 0)

        colors.colored("Network Protection disabled successfully. If you are still restricted, try restarting your computer or executing command again.", colors.OKBLUE)
    except PermissionError:
        colors.fail("Permission denied. Please run this program as an administrator.")
    except Exception as e:
        colors.fail(f"An error occurred: {e}")