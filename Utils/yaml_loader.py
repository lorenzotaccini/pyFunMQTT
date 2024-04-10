import yaml
import yaml as y
import CLI as cli


class YamlLoader:
    def __init__(self):
        self.runargs = cli.CLI()


with open("..\\Tests\\Test.yaml") as stream:
    try:
        print(yaml.safe_load("unbalanced blackets: ]["))
    except yaml.YAMLError as exc:
        if hasattr(exc, 'problem_mark'):
            print(f"Error in YAML file {stream.name}, line {exc.problem_mark.line + 1}")
        else:
            print(exc)
