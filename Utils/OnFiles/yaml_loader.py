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
                    if self.check_structure(yamlres):
                        print("successfully loaded YAML config file: " + self.configfile)
                        return yamlres
                    else:
                        return None
                except y.YAMLError as exc:  # exception on YAML syntax
                    if hasattr(exc, 'problem_mark'):
                        print(f"Error in YAML file {stream.name}, line {exc.problem_mark.line + 1}", file=sys.stderr)
                    else:
                        print(exc)
        except FileNotFoundError:
            print("Config file not found, maybe incorrect path?", file=sys.stderr)
            return None

    # class method to check correct fields spelling and presence
    @staticmethod
    def check_structure(yaml_content: dict) -> bool:
        required_fields = {'broker': r"^(((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4})$|^localhost$",
                           'port': r"^(?:[1-9]\d{0,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$",
                           'topic': r"^([a-zA-Z0-9_\-#]+/?)*[a-zA-Z0-9_\-#]+$",
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

            if isinstance(value, list):
                for v in value:
                    if not re.match(pattern, v):
                        wrong_fields.append(field)
            else:
                if not re.match(pattern, str(value)):
                    wrong_fields.append(field)

        if wrong_fields:
            raise ValueError(f"the following fields are wrong or missing: {wrong_fields}")
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
