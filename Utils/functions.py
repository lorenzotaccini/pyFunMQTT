class MethodToolBox:
    def fun1(self):
        print("fun1!")

    def fun2(self):
        print("fun2!")

    @classmethod
    def is_in_toolbox(cls, fun_name: str) -> bool:
        return hasattr(cls, fun_name) and callable(getattr(cls, fun_name))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="This tool allows you to search for a function in the toolbox "
                                                 "directly from command line, to check its presence.")
    parser.add_argument("method_name", metavar='M',
                        help="name of the method you want to search in the toolbox")
    method_name = parser.parse_args().method_name
    print(f"Method {method_name} is {"not " if not MethodToolBox.is_in_toolbox(method_name) else ""}"
          f"in Methods ToolBox")
