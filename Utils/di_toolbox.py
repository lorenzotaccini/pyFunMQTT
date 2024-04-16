import time
from typing import Any
from user_functions import Service


class MethodToolBox:

    def __init__(self):
        self.services = {cls.__name__: cls() for (cls) in Service.__subclasses__()}


    def run(self, data: Any) -> Any:
        print()
        #for s in self.services:
        #    out = s.serve(out)
        #return out


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Simple CLI tool to check whether a method with given name is in the "
                                                 "Methods ToolBox or not.")
    parser.add_argument("method_name", metavar='M',
                        help="name of the method you want to search in the toolbox")
    method_name = parser.parse_args().method_name

    print(f"Class {method_name} is {"not " if method_name not in MethodToolBox().services.keys() else ""}"
          f"in Methods ToolBox")
