# Disables Windows Defender Signature Check
import winreg
from EasyMenu3 import colors

# Module metadata
NAME = "Disable Signature Check"
DESC = "Disables Windows Defender Signature Check. Should allow execution of unsigned files and possibly some blocked apps."

# Variables
PATHS = {
    1: { # Defender key
        "path": r"SOFTWARE\Policies\Microsoft\Windows Defender\Policy Manager",
        "key": "CheckForSignaturesBeforeRunningScan"
    },
    2: { # Intune key
        "path": r"\SOFTWARE\Microsoft\PolicyManager\current\device\Defender",
        "key": "CheckForSignaturesBeforeRunningScan_WinningProvider"
    }
}

HKEY_LOC = winreg.HKEY_LOCAL_MACHINE

def run():
    reg = winreg.ConnectRegistry(None, HKEY_LOC)
    defender_key = PATHS[1]
    intune_key = PATHS[2]

    try:
        # Disable Defender Signature Check
        with winreg.OpenKey(reg, defender_key["path"], 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, defender_key["key"], 0, winreg.REG_DWORD, 0)

        # Disable Intune Signature Check
        with winreg.OpenKey(reg, intune_key["path"], 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, intune_key["key"], 0, winreg.REG_DWORD, 0)

        colors.colored("Signature Check disabled successfully. If you are still restricted, try restarting your computer or executing command again.", colors.OKBLUE)
    except PermissionError:
        colors.fail("Permission denied. Please run this program as an administrator.")
    except Exception as e:
        colors.fail(f"An error occurred: {e}")