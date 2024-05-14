from Utils.OnFiles.yaml_loader_full import YamlLoader as y

if __name__ == '__main__':
    loader = y('config.yml').load()
    for i in loader:
        print(i)
