import os
import time

class FileWatchdog:
    def __init__(self, filename):
        self.filename = filename
        self.last_modified_time = self.get_last_modified_time()

    def get_last_modified_time(self):
        if os.path.exists(self.filename):
            return os.path.getmtime(self.filename)
        else:
            raise FileNotFoundError(f"{self.filename} does not exist.")

    def check_modification(self):
        current_modified_time = self.get_last_modified_time()
        if current_modified_time != self.last_modified_time:
            print(f"File {self.filename} has been modified.")
            self.last_modified_time = current_modified_time

    def watch(self, interval=1):
        while True:
            self.check_modification()
            time.sleep(interval)

# Example usage:
if __name__ == "__main__":
    filename = "config.yml"  # Replace with the file you want to watch
    watchdog = FileWatchdog(filename)
    watchdog.watch()