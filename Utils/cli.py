import argparse
import os


class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="PyFunMQTT")
        self.parser.add_argument("-c", "--configfile",
                                 default=str(
                                     os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Tests',
                                                  'config.yml')),
                                 help="load config file in YAML format (default: config.yml in Tests folder)")
        self.parser.add_argument("-v", "--verbose", default=True, action='store_true', help='verbose mode, allows to '
                                                                                            'see all traffic'
                                                                                            'being processed by the '
                                                                                            'clients')
        self.parser.add_argument('-s', '--silent', default=False, action='store_true', help='disable all stdout and '
                                                                                            'stderr logging. File '
                                                                                            'logging is still enabled')
        self.parser.add_argument("-w", default=10, help="wait time in seconds between watchdog scans on given "
                                                        "configuration file")
        self.args = self.parser.parse_args()


if __name__ == "__main__":
    cli = CLI()
    print(cli.args)
