import argparse
import os


class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="PyFunMQTT")

        silent_verbose_group = self.parser.add_mutually_exclusive_group()

        self.parser.add_argument("-c", "--configfile",
                                 default=str(
                                     os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Tests',
                                                  'config.yml')),
                                 help="load config file in YAML format (default: config.yml in Tests folder)")
        silent_verbose_group.add_argument("-v", "--verbose",
                                          default=True,
                                          action='store_true',
                                          help='verbose mode, allows to see all the traffic ')
        silent_verbose_group.add_argument('-s',
                                          '--silent',
                                          default=False,
                                          action='store_true',
                                          help='disable all stdout and stderr logging. File logging is still enabled')
        self.parser.add_argument('--log-messages',
                                 default=False,
                                 action='store_true',
                                 help='enable logging messages on separate log file. Note that program\'s performance '
                                      'will be negatively affected by this')
        self.parser.add_argument("-w",
                                 default=10,
                                 help="wait time in seconds between watchdog scans on given configuration file")
        self.args = self.parser.parse_args()


if __name__ == "__main__":
    cli = CLI()
    print(cli.args)
