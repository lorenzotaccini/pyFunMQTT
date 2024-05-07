import sys
import yaml as y
import re


class YamlLoader:
    def __init__(self, configfile_name: str):
        self.configfile_name = configfile_name

    def load(self) -> [dict | None]:
        try:
            with open(self.configfile_name) as stream:
                yamlres = y.safe_load(stream)
                if YamlLoader.check_structure(yamlres):
                    print("successfully loaded YAML config file: " + self.configfile_name)
                    return yamlres
                else:
                    print("YAML config file not loaded")
                    sys.exit(-1)
        except FileNotFoundError:
            print("Config file not found, maybe incorrect path?", file=sys.stderr)
            return None
        except y.YAMLError as exc:  # exception on YAML syntax
            if hasattr(exc, 'problem_mark'):
                print(f"Error in YAML file {stream.name}, line {exc.problem_mark.line + 1}", file=sys.stderr)
            else:
                print(exc)

    # static method to check correct fields spelling and presence
    @staticmethod
    def check_structure(yaml_content: dict) -> bool:
        required_fields = {'broker': r"^(((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4})$|^localhost$",
                           'port': r"^(?:[1-9]\d{0,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$",
                           'inTopic': r"^([a-zA-Z0-9_\-#]+/?)*[a-zA-Z0-9_\-#]+$",
                           'outTopic': r"^([a-zA-Z0-9_\-#]+/?)*[a-zA-Z0-9_\-#]+$",
                           'function': r"^([a-zA-Z0-9_\-])+$",
                           'key': r"^([a-zA-Z0-9_\-])+$",
                           'outFormat': r'\b(json|xml|yaml|csv)\b',
                           'inFormat': r'\b(json|xml|yaml|csv)\b'}

        # catches and enlightens missing keys from YAML file
        wrong_fields = []

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
        try:
            if wrong_fields:
                raise ValueError()
            else:
                print("configuration file is valid", end='')
            # all checked, return True
            print(" -> end of spell checking")
            return True
        except ValueError:
            print(f"the following fields are wrong or missing: {wrong_fields}")
            return False
