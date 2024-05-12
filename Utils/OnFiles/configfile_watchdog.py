import os
import time
from datetime import datetime


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
                         f"with new parameters? (y/n) ->  ")
            if flag == 'y' or flag == 'Y':
                self.stop_flag = True
            self.last_modified_time = current_modified_time

    def watch(self, interval=1):
        while not self.stop_flag:
            self.check_modification()
            time.sleep(interval)
        self.worker.reload()
        return True


# Example usage:
if __name__ == "__main__":
    filename = "config.yml"  # Replace with the file you want to watch
    watchdog = ConfigFileWatchdog(filename)
    watchdog.watch()
