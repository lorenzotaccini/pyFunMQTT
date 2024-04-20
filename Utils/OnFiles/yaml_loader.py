import sys
import yaml as y
import Utils.cli as cli
import re


class YamlLoader:
    def __init__(self):
        self.runargs = cli.CLI()
        self.configfile = self.runargs.args.configfile

    def load(self) -> [dict | None]:
        try:
            with open(self.configfile) as stream:
                try:
                    yamlres = y.safe_load(stream)
                    print("successfully loaded YAML config file: " + self.configfile)
                    if self.check_structure(yamlres):
                        return yamlres
                    else:
                        return None
                except y.YAMLError as exc:  # exception on YAML syntax
                    if hasattr(exc, 'problem_mark'):
                        print(f"Error in YAML file {stream.name}, line {exc.problem_mark.line + 1}", file=sys.stderr)
                    else:
                        print(exc)
        except FileNotFoundError:
            print("Config file not found, maybe incorrect path?")
            return None

    # class method to check correct fields spelling and presence
    @staticmethod
    def check_structure(yaml_content: dict) -> bool:
        required_fields = {'topic': r"^([a-zA-Z0-9_\-#]+/?)*[a-zA-Z0-9_\-#]+$",
                           'outTopic': r"^([a-zA-Z0-9_\-#]+/?)*[a-zA-Z0-9_\-#]+$",
                           'function': r"^([a-zA-Z0-9_\-])+$",
                           'key': r"^([a-zA-Z0-9_\-])+$",
                           'outFormat': r'\b(json|xml|yaml)\b',
                           'inFormat': r'\b(json|xml|yaml)\b'}

        wrong_fields = []
        # catches and enlightens missing keys from YAML file

        print("\nspell checking -> ", end='')
        # check input topic
        for field, pattern in required_fields.items():
            if field not in yaml_content:
                wrong_fields.append(field)
                continue

            value = yaml_content[field]

            # if
            if isinstance(value, list):
                for v in value:
                    if not re.match(pattern, v):
                        wrong_fields.append(field)
            else:
                if not re.match(pattern, value):
                    wrong_fields.append(field)

        if wrong_fields:
            print(f"the following fields are wrong or missing: {wrong_fields}", file=sys.stderr, end='')
            return False
        else:
            print("configuration file is valid", end='')
        # all checked, return True
        print(" -> end of spell checking")
        return True


if __name__ == "__main__":
    yl = YamlLoader()
    confstruct = yl.load()
    print(confstruct)
    YamlLoader.check_structure(confstruct)
