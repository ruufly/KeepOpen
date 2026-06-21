import winreg
import os, sys
import json
import subprocess


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


def getpath():
    return os.path.realpath(sys.executable)
    # return os.path.abspath(__file__)


def getdir(dir):
    return os.path.join(os.path.dirname(getpath()), dir)


if not os.path.exists(getdir("data\\setting.json")):
    with open(
        getdir("data\\setting.json"),
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

with open(getdir("data\\setting.json"), "r", encoding="utf-8") as f:
    setting = json.load(f)

if setting["Start"]:
    add_to_startup("KeepOpenStartup", getpath())
else:
    remove_from_startup("KeepOpenStartup")

print(setting)
print(getdir("main_uac.exe"))

if setting["Administer"]:
    os.system(getdir("main_uac.exe"))
else:
    os.system(getdir("main.exe"))
