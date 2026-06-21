#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import os.path
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
from plyer import notification
import threading
import psutil
import sys


def getdir(dir):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), dir)

def getpartition():
    partitions = []
    for partition in psutil.disk_partitions():
        partitions.append(partition.mountpoint)
    return tuple(partitions)


class KeepOpen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title("KeepOpen")
        self.root.iconbitmap(getdir("data\\icon.ico"))
        self.root.geometry("300x200")

        self.root.protocol("WM_DELETE_WINDOW", self.hide_to_tray)

        self.create_tray_icon()

        notification.notify(
            title="KeepOpen",
            message="KeepOpen已最小化至系统托盘",
            app_name="KeepOpen",
            app_icon=getdir("data\\icon.ico"),
        )

    def create_tray_icon(self):
        image = Image.open(getdir("data\\smallest.dat"))

        menu = (
            item("打开", self.show_app, default=True),
            item("退出", self.quit_app),
        )

        self.tray_icon = pystray.Icon("hidden_app", image, "KeepOpen", menu)

    def show_app(self, icon=None, item=None):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def hide_to_tray(self):
        self.root.withdraw()

    def quit_app(self, icon=None, item=None):
        self.tray_icon.stop()
        self.root.quit()
        sys.exit(0)

    def run(self):
        def run_tray():
            self.tray_icon.run()

        tray_thread = threading.Thread(target=run_tray, daemon=True)
        tray_thread.start()

        self.root.mainloop()


if __name__ == "__main__":
    app = KeepOpen()
    app.run()
