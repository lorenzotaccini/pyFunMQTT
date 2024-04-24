from typing import Any
from Utils.UserFunctions.user_functions import Service


class MethodToolBox:

    def __init__(self):
        self.services = {str.lower(cls.__name__): cls() for cls in Service.__subclasses__()}

    def process(self, func_name: [str], data: Any) -> Any:
        for f in func_name:
            if f in self.services.keys():
                data = self.services[f].serve(data)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Simple CLI tool to check whether a method with given name is in the "
                                                 "Methods ToolBox or not.")
    parser.add_argument("method_name", metavar='M',
                        help="name of the method you want to search in the toolbox")
    method_name = parser.parse_args().method_name

    print(f"Class {str.lower(method_name)} is "
          f"{"not " if str.lower(method_name) not in MethodToolBox().services.keys() else ""}"
          f"in Methods ToolBox")
