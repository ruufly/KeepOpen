import winreg
import os, sys
import json
from goto import with_goto


def add_to_startup(name, file_path=""):
    if file_path == "":
        file_path = os.path.realpath(sys.argv[0])
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        0,
        winreg.KEY_SET_VALUE,
    )
    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, file_path)
    winreg.CloseKey(key)


def remove_from_startup(name):
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        0,
        winreg.KEY_SET_VALUE,
    )
    try:
        winreg.DeleteValue(key, name)
    except FileNotFoundError:
        pass
    winreg.CloseKey(key)


dirpath = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists(os.path.join(dirpath, "data\\setting.json")):
    with open(
        os.path.join(dirpath, "data\\setting.json"),
        "w",
        encoding="utf-8",
    ) as f:
        setting = {
            "MountPoints": [],
            "Filename": ".keepopen",
            "Waiting": 30,
            "Start": True,
            "Administer": False,
        }
        json.dump(f, setting)

with open(os.path.join(dirpath, "data\\setting.json"), "r", encoding="utf-8") as f:
    setting = json.load(f)

if setting["Start"]:
    add_to_startup("KeepOpenStartup", os.path.abspath(__file__))
else:
    remove_from_startup("KeepOpenStartup")

@with_goto
def run():
    if setting["Administer"]:
        import main
    else:
        import main
