import yaml as y
import CLI as cli


class YamlLoader:
    def __init__(self):
        self.runargs = cli.CLI()


with open("../Tests/config.yml") as stream:
    try:
        print(y.safe_load(stream))
    except y.YAMLError as exc:
        if hasattr(exc, 'problem_mark'):
            print(f"Error in YAML file {stream.name}, line {exc.problem_mark.line + 1}")
        else:
            print(exc)
