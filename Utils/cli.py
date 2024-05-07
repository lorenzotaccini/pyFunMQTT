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
        self.parser.add_argument("-p", "--port",
                                 help="connection port on which the broker is operating")
        self.parser.add_argument("-b", "--broker", default="localhost",
                                 help="broker's IP address (default: localhost)")
        self.parser.add_argument("-t", "--topic", default="nomedefaulttopic",
                                 help="topic on which you're listening (default: nomedefaulttopic)")
        self.parser.add_argument("-s", "--silent", default=False, help="suppress all console output except "
                                                                       "for when the program needs to communicate "
                                                                       "with the user")
        self.args = self.parser.parse_args()


if __name__ == "__main__":
    cli = CLI()
    print(cli.args)
