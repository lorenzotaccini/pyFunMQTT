import os
import time
from datetime import datetime


# not using watchdog library as of now, it was resulting in the watchdog thread being unable to detect file changes
class ConfigFileWatchdog:
    def __init__(self, worker):
        self.worker = worker
        self.filename = self.worker.configfile_name
        self.last_modified_time = self.get_last_modified_time()
        self.stop_flag = False

    def get_last_modified_time(self):
        if os.path.exists(self.filename):
            return os.path.getmtime(self.filename)
        else:
            raise FileNotFoundError(f"{self.filename} does not exist.")

    def check_modification(self):
        current_modified_time = self.get_last_modified_time()
        if current_modified_time != self.last_modified_time:
            # Get the current time
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            flag = input(f"{formatted_time}: detected changes in config file {self.filename}, reload configuration "
                         f"with new parameters? [y/n] ->  ")
            if flag == 'y' or flag == 'Y':
                self.stop_flag = True
            self.last_modified_time = current_modified_time

    def watch(self, interval=1):
        while True:
            while not self.stop_flag:
                if self.worker.watchdog_stop_event.is_set():
                    return True
                time.sleep(interval)
                self.check_modification()
            self.worker.reload()
            self.stop_flag = False
