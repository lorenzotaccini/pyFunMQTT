
import argparse


class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="PyFunMQTT")
        self.parser.add_argument("-c", "--configfile", default="config.yml",
                                 help="load config file in YAML format (default: config.yml in Tests folder)")
        self.parser.add_argument("-p", "--port",
                                 help="connection port on which the broker is operating")
        self.parser.add_argument("-b", "--broker", default="localhost",
                                 help="broker's IP address (default: localhost)")
        self.parser.add_argument("-t", "--topic", default="nomedefaulttopic",
                                 help="topic on which you're listening (default: nomedefaulttopic)")
        self.args = self.parser.parse_args()


if __name__ == "__main__":
    cli = CLI()
    print(cli.args)