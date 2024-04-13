import sys

import yaml as y
import cli as cli
import inspect
import re


class YamlLoader:
    def __init__(self):
        self.runargs = cli.CLI()
        self.configfile = self.runargs.args.configfile

    def load(self) -> dict:
        try:
            with open(self.configfile) as stream:
                try:
                    yamlres = y.safe_load(stream)
                    print("successfully loaded YAML config file")
                    return yamlres
                except y.YAMLError as exc:
                    if hasattr(exc, 'problem_mark'):
                        print(f"Error in YAML file {stream.name}, line {exc.problem_mark.line + 1}")
                    else:
                        print(exc)
        except FileNotFoundError:
            print("config file not found, maybe incorrect path?")

    # class method to check correct fields spelling and presence
    @classmethod
    def check_structure(cls, yaml_content: dict) -> bool:
        topic_matcher = r"^([a-zA-Z0-9_\-#]+/?)*[a-zA-Z0-9_\-#]+$"
        function_matcher = r"^([a-zA-Z0-9_\-])+$"
        key_matcher = r"^([a-zA-Z0-9_\-])+$"
        out_format_matcher = ['json', 'yaml', 'xml']

        # catches and enlightens missing keys from YAML file
        try:
            # check input topic
            if re.fullmatch(topic_matcher, yaml_content['topic']):
                print("input topic correct")
            else:
                print("wrong format for input topic", file=sys.stderr)
                return False

            # check output topic
            if re.fullmatch(topic_matcher, yaml_content['outTopic']):
                print("output topic correct")
            else:
                print("wrong format for output topic", file=sys.stderr)
                return False

            # check function names
            for i, f in enumerate(yaml_content['function']):
                if re.fullmatch(function_matcher, f):
                    print(f"function {i} correct")
                else:
                    print(f"wrong format for function: {f}", file=sys.stderr)
                    return False

            # check for correct output format
            if yaml_content['outFormat'] in out_format_matcher:
                print("output format allowed")
            else:
                print("wrong output format specified", file=sys.stderr)
                return False

            # check for optional key value, False not returned in that case
            if 'key' in yaml_content:  # key field is optional
                if re.fullmatch(key_matcher, yaml_content['key']):
                    print("key correct")
                else:
                    print("wrong format for key", file=sys.stderr)
            else:
                print("key field not present")
        except KeyError as k:
            print(f"some required keys are missing from YAML config file: {k.args}", file=sys.stderr)
        # all checked, return True
        return True


if __name__ == "__main__":
    yl = YamlLoader()
    confstruct = yl.load()
    YamlLoader.check_structure(confstruct)
