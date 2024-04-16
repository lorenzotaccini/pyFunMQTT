import sys


#OLD VERSION

import user_functions as uf
import inspect


# class that contains
class MethodToolBox:
    def __init__(self):
        self.classes = [cls_name for cls_name, cls_obj in inspect.getmembers(uf) if inspect.isclass(cls_obj)]
        self.methods = [func_name for func_name, func_obj in inspect.getmembers(uf) if inspect.ismethod(func_obj)]
        print(self.classes)


    @classmethod
    def is_in_toolbox(cls, fun_name: str) -> bool:
        return hasattr(cls, fun_name) and callable(getattr(cls, fun_name))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simple CLI tool to check whether a method with given name is in the "
                                                 "Methods ToolBox or not.")
    parser.add_argument("method_name", metavar='M',
                        help="name of the method you want to search in the toolbox")
    method_name = parser.parse_args().method_name
    print(f"Method {method_name} is {"not " if not MethodToolBox.is_in_toolbox(method_name) else ""}"
          f"in Methods ToolBox")