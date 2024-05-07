import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import Utils.cli as cli


class ConfigFileWatchdog(FileSystemEventHandler):
    def __init__(self, run_args=cli.CLI()):
        super().__init__()
        self.run_args = run_args
        self.configfile = self.run_args.args.configfile

    def on_modified(self, event):
        if event.src_path.endswith(self.configfile):
            print(f"{time.localtime()}-> Detected changes in actual configuration file: '{self.configfile}'"
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
