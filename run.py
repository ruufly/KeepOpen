import winreg
import os, sys
import json
import psutil
from plyer import notification
import subprocess
import ctypes


def is_process_running(process_name):
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == process_name:
            return True
    return False


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


if is_process_running("keepopen_main_uac.exe") or is_process_running(
    "keepopen_main.exe"
):
    notification.notify(
        title="KeepOpen",
        message="KeepOpen正在运行，请勿重复打开！",
        app_name="KeepOpen",
        app_icon=getdir("data\\icon.ico"),
    )
else:
    if setting["Administer"]:
        if ctypes.windll.shell32.IsUserAnAdmin():
            subprocess.run([getdir("keepopen_main_uac.exe")])
        else:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
    else:
        subprocess.run([getdir("keepopen_main.exe")])
