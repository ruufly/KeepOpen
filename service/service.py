import os
import logging
import shutil
import inspect
import json


class Service():
    def __init__(self):
        self.logger = self._getLogger()
        self.run = True
        self._flush()

    def _flush(self):
        # self.dirpath = os.path.abspath(
        #     os.path.dirname(inspect.getfile(inspect.currentframe()))
        # )
        self.dirpath = os.path.dirname(os.path.abspath(__file__))
        displayFile = os.path.join(self.dirpath, "..\\data\\running.tmp")
        with open(displayFile, "w") as f:
            pass

        if not os.path.exists(os.path.join(self.dirpath, "..\\data\\setting.json")):
            self.logger.warning("cannot read the setting file")
            with open(
                os.path.join(self.dirpath, "..\\data\\setting.json"),
                "w",
                encoding="utf-8",
            ) as f:
                self.setting = {
                    "MountPoints": [],
                    "Filename": ".keepopen",
                    "Waiting": 30,
                    "Start": True,
                    "Administer": False,
                }
                json.dump(f, self.setting)

        with open(
            os.path.join(self.dirpath, "..\\data\\setting.json"), "r", encoding="utf-8"
        ) as f:
            self.setting = json.load(f)

        self.MountPoints = self.setting["MountPoints"]
        self.Filename = self.setting["Filename"]
        self.Waiting = self.setting["Waiting"]

        if os.path.exists(displayFile):
            os.remove(displayFile)

    def _getLogger(self):
        logger = logging.getLogger("[KeepOpen]")

        self._flush()
        handler = logging.FileHandler(os.path.join(self.dirpath, "service.log"))

        formatter = logging.Formatter(
            "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger

    def SvcDoRun(self):
        import time

        self.logger.info("service is start")
        self._flush()
        self.logger.info(f"start at: {self.dirpath}")
        while self.run:
            displayFile = os.path.join(self.dirpath, self.Filename)
            with open(displayFile, "w") as f:
                pass
            self.logger.info("copying files...")
            for i in self.MountPoints:
                try:
                    shutil.copy(displayFile, os.path.join(i,self.Filename))
                    self.logger.info(f"    finish to copy the file to {i}")
                except Exception as e:
                    self.logger.error(f"    error to copy the file to {i}: {e}")
            self.logger.info("    done.")
            self.logger.info("waiting for the next cycle...")
            time.sleep(self.Waiting)

Service().SvcDoRun()