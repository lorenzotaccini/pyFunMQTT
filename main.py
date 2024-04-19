from Utils.yaml_loader import YamlLoader
from Utils.toolbox import MethodToolBox

if __name__ == '__main__':
    y = YamlLoader()
    config_info = y.load()
    YamlLoader.check_structure(config_info)

    m = MethodToolBox()
    m.run(config_info['function'][0], config_info['topic'])
