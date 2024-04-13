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

    @classmethod
    def check_structure(cls, yaml_content: dict) -> bool:
        topic_matcher = r"^([a-zA-Z0-9_-]+/?)*[a-zA-Z0-9_-]+$"

        if re.fullmatch(topic_matcher, yaml_content['topic']):
            print("topic correct")
        return True


if __name__ == "__main__":
    yl = YamlLoader()
    confstruct = yl.load()
    print(confstruct)
    YamlLoader.check_structure(confstruct)
