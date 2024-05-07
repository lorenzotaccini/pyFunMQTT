import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import Utils.cli as cli


class ConfigFileWatchdog(FileSystemEventHandler):
    def __init__(self, configfile_name: str):
        super().__init__()
        self.configfile_name = configfile_name

    def on_modified(self, event):
        if event.src_path.endswith(self.configfile_name):
            print(f"at {time.localtime()} -> Detected changes in actual configuration file: '{self.configfile_name}'"
                  f"\nReload the session applying the new configuration? [y/n]: ")

    def watch(self):
        observer = Observer()
        observer.schedule(self, path='.', recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


# Example usage:
if __name__ == "__main__":
    file_watcher = ConfigFileWatchdog("config.yml")
    file_watcher.watch()
