#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import os.path
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw, ImageTk
from plyer import notification
import threading
import json
import psutil
import os, sys
import shutil
import logging


def getpath():
    return os.path.dirname(os.path.realpath(sys.executable))
    # return os.path.dirname(os.path.abspath(__file__))


def getdir(dir):
    return os.path.join(getpath(), dir)


def getpartition():
    partitions = []
    for partition in psutil.disk_partitions():
        partitions.append(partition.mountpoint)
    return tuple(partitions)


def getsetting():
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
            json.dump(setting, f)

    with open(getdir("data\\setting.json"), "r", encoding="utf-8") as f:
        setting = json.load(f)

    if not (
        "MountPoints" in setting
        and "Filename" in setting
        and "Waiting" in setting
        and "Start" in setting
        and "Administer" in setting
    ):
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
            json.dump(setting, f)

    return setting


class Service(object):
    def __init__(self):
        self.logger = logging.getLogger("[KeepOpen]")

        self.flush()
        handler = logging.FileHandler(getdir("service.log"))

        formatter = logging.Formatter(
            "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        )
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        self.flush()

    def flush(self):
        self.dirpath = getpath()
        # while os.path.exists(getdir("data\\running.tmp")):
        #     pass

        self.setting = getsetting()

        self.MountPoints = self.setting["MountPoints"]
        self.Filename = self.setting["Filename"]
        self.Waiting = self.setting["Waiting"]

    def log(self, type, message):
        getattr(self.logger, type)(message)

    def Run(self):
        import time

        self.logger.info("service is starting")
        self.flush()
        self.logger.info(f"start at: {self.dirpath}")
        while serviceRun:
            self.flush()
            displayFile = os.path.join(self.dirpath, self.Filename)
            with open(displayFile, "w") as f:
                pass
            self.logger.info("copying files...")
            for i in self.MountPoints:
                try:
                    shutil.copy(displayFile, os.path.join(i, self.Filename))
                    self.logger.info(f"    finished to copy the file to {i}")
                except Exception as e:
                    self.logger.error(f"    failed to copy the file to {i}: {e}")
            self.logger.info("    done.")
            self.logger.info("waiting for the next cycle...")
            time.sleep(self.Waiting)


global serviceRun
serviceRun = True

global service
service = Service()
service.log("info", "Nyahoo~")

global main
main = threading.Thread(target=service.Run)


class KeepOpen:
    def __init__(self):
        self.setting = getsetting()
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title("KeepOpen 设置")
        self.root.iconbitmap(getdir("data\\icon.ico"))
        self.root.geometry("500x300")
        self.root.resizable(width=0, height=0)
        self.root.configure(background="white")

        global symbol_unchecked
        symbol_unchecked = ImageTk.PhotoImage(
            Image.open(
                getdir(
                    os.path.join("data", "MaterialSymbolsLightCheckBoxOutlineBlank.png")
                )
            ).resize((20, 20))
        )

        global symbol_checked
        symbol_checked = ImageTk.PhotoImage(
            Image.open(
                getdir(
                    os.path.join(
                        "data",
                        "MaterialSymbolsLightCheckBoxOutlineRounded.png",
                    )
                )
            ).resize((20, 20))
        )

        self.TreeFrame = tk.Frame(self.root)
        self.TreeList = ttk.Treeview(self.TreeFrame, columns=["mountpoint"])
        self.TreeList.tag_configure("fggrey", foreground="grey")

        self.yScroll = ttk.Scrollbar(
            self.TreeFrame, orient=tk.VERTICAL, command=self.TreeList.yview
        )
        self.yScroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.xScroll = ttk.Scrollbar(
            self.TreeFrame, orient=tk.HORIZONTAL, command=self.TreeList.xview
        )
        self.xScroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.TreeList.config(yscrollcommand=self.yScroll.set)
        self.TreeList.config(xscrollcommand=self.xScroll.set)
        self.TreeList.tag_configure("checked", image=symbol_checked)
        self.TreeList.tag_configure("unchecked", image=symbol_unchecked)

        self.TreeList.heading("mountpoint", text="盘符挂载点")

        self.seqs, self.rs = [], 0
        for i in getpartition():
            self.seqs.append(self.TreeList.insert("", "end", text=i, values=i))
            self.TreeList.item(
                self.seqs[self.rs],
                tags=("checked" if i in self.setting["MountPoints"] else "unchecked",),
            )
            self.rs += 1

        self.TreeList.bind("<<TreeviewSelect>>", self.on_checkbox_changed)

        self.TreeList.pack(fill=tk.BOTH, expand=1)

        self.TreeFrame.place(relwidth=1, relheight=0.5, relx=0, rely=0)

        tk.Label(self.root, text="刷新时间（秒）", bg="white").place(
            relx=0.05, rely=0.55
        )

        self.current_value = tk.StringVar(value=str(self.setting["Waiting"]))
        self.Spin = ttk.Spinbox(
            self.root,
            from_=10,
            to=120,
            increment=10,
            textvariable=self.current_value,
            wrap=True,
        )
        self.Spin.place(relwidth=0.55, relx=0.25, rely=0.55)

        self.style = ttk.Style(self.root)
        self.style.configure("TCheckbutton", background="white")

        self.CheckVar1 = tk.IntVar()
        self.CheckVar2 = tk.IntVar()
        self.CheckVar1.set(self.setting["Start"])
        self.CheckVar2.set(self.setting["Administer"])
        self.C1 = ttk.Checkbutton(
            self.root, text="开机自启动", variable=self.CheckVar1, onvalue=1, offvalue=0
        )
        self.C2 = ttk.Checkbutton(
            self.root,
            text="以管理员模式启动",
            variable=self.CheckVar2,
            onvalue=1,
            offvalue=0,
        )
        self.C1.place(relx=0.05, rely=0.65)
        self.C2.place(relx=0.5, rely=0.65)

        self.ButtonOkay = ttk.Button(self.root, text="确定", command=self._buttonOkay)
        self.ButtonCan = ttk.Button(self.root, text="取消", command=self._buttonCancel)
        self.ButtonAbout = ttk.Button(self.root, text="关于", command=self._buttonAbout)
        self.ButtonDel = ttk.Button(self.root, text="清理缓存", command=self._buttonDel)
        self.ButtonDel.place(relx=0.2, rely=0.85)
        self.ButtonAbout.place(relx=0.4, rely=0.85)
        self.ButtonCan.place(relx=0.6, rely=0.85)
        self.ButtonOkay.place(relx=0.8, rely=0.85)

        self.root.protocol("WM_DELETE_WINDOW", self.hide_to_tray)

        service.log("info", "finished to initialize the window")

        self.create_tray_icon()

    def _buttonOkay(self, *args):
        self.setting["Start"] = bool(self.CheckVar1.get())
        self.setting["Administer"] = bool(self.CheckVar2.get())
        try:
            self.setting["Waiting"] = int(self.current_value.get())
        except Exception as e:
            service.log("error", f"failed to change the setting: {e}")
            messagebox.showerror("KeepOpen", f"设置失败：{e}")
            return
        self.setting["MountPoints"] = []
        for i in self.TreeList.get_children():
            if self.TreeList.item(i, "tag")[0] == "checked":
                self.setting["MountPoints"].append(self.TreeList.item(i, "values")[0])
        messagebox.showinfo("KeepOpen", "设置成功！部分设置项可能需要重启以应用")
        self.root.withdraw()
        service.log("info", "the setting is confirmed")
        service.setting = self.setting
        with open(
            getdir("data\\setting.json"),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(self.setting, f)
        service.log("info", "the setting is saved")

    def _buttonCancel(self, *args):
        self.root.withdraw()
        service.log("info", "the setting is canceled")

    def _buttonAbout(self, *args):
        about = tk.Toplevel(self.root)
        about.title("关于")
        about.geometry("800x315")
        about.resizable(width=0, height=0)
        about.configure(background="#fceedb")

        global image_ban
        image_ban = ImageTk.PhotoImage(
            Image.open(
                getdir(
                    os.path.join(
                        "data",
                        "image.png",
                    )
                )
            )
        )
        tk.Label(about, image=image_ban, bg="#fceedb").place(x=0, y=0)
        tk.Label(
            about,
            anchor="w",
            justify="left",
            text="""KeepOpen v1.0
一款维持某一盘符的活动状态以防止移动硬盘自动休眠的小工具

Copyright 2026 distjr_

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

git: https://github.com/ruufly/KeepOpen.git""",
            bg="#fceedb",
        ).place(x=300, y=0)

    def _buttonDel(self, *args):
        service.log("info", "deleting the caches")
        with open(getdir("service.log"), "w") as f:
            pass
        messagebox.showinfo("KeepOpen", "清理成功！")
        service.log("info", "delete the caches: done")

    def on_checkbox_changed(self, *args):
        item_id = self.TreeList.focus()
        now_get = self.TreeList.item(item_id, "text")
        checkbox_state = self.TreeList.item(item_id, "tag")
        if (
            os.path.samefile(now_get, os.path.join(os.environ.get("SystemDrive"), "/"))
            and (checkbox_state[0] == "unchecked")
            and (not bool(self.CheckVar2.get()))
        ):
            messagebox.showinfo("KeepOpen", "该盘符为系统盘，建议同时勾选管理员模式！")
        if checkbox_state[0] == "checked":
            self.TreeList.item(item_id, tags=("unchecked",))
        else:
            self.TreeList.item(item_id, tags=("checked",))

    def create_tray_icon(self):
        image = Image.open(getdir("data\\smallest.ico"))

        menu = (
            item("设置", self.show_app, default=True),
            item("退出", self.quit_app),
        )

        self.tray_icon = pystray.Icon("hidden_app", image, "KeepOpen", menu)

    def show_app(self, icon=None, item=None):
        service.log("info", "the setting window is opened")
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def hide_to_tray(self):
        self.root.withdraw()

    def quit_app(self, icon=None, item=None):
        global serviceRun
        self.tray_icon.stop()
        service.log("info", "closing the service...")
        self.root.quit()
        serviceRun = False
        service.log("info", "Byenya~")
        os._exit(0)

    def run(self):
        def run_tray():
            self.tray_icon.run()

        # self.tray_icon.HAS_NOTIFICATION = True
        # self.tray_icon.notify('服务已启动，KeepOpen已最小化至系统托盘', 'KeepOpen')
        tray_thread = threading.Thread(target=run_tray, daemon=True)
        tray_thread.start()

        main.start()

        notification.notify(
            title="KeepOpen",
            message="服务已启动，KeepOpen已最小化至系统托盘",
            app_name="KeepOpen",
            app_icon=getdir("data\\icon.ico"),
        )

        service.log("info", "initialization is done.")

        self.root.mainloop()


app = KeepOpen()
app.run()
