from abc import ABC, abstractmethod
from typing import Any


class Service(ABC):
    @abstractmethod
    def serve(self, conf: dict, data: Any) -> Any:
        ...


# USER DEFINED CLASSES

class RemoveWS(Service):
    def serve(self, conf, data: str):
        return data.replace(' ', '')


# input: list of dict, output: dict{outtopic: payload}
class SplitCols(Service):
    def serve(self, conf: dict, data: list) -> dict:
        res = {}
        for elem in data:  # for every row (a row is a dict)
            for k, v in elem.items():  # for every column
                if k in conf['parameters']:
                    if k not in res.keys():
                        res[k] = []
                    res[k].append(v)
        return res


class Upper(Service):
    def serve(self, conf, data: str):
        return str(data).upper()


class Extract(Service):
    def serve(self, conf, data: Any):
        pass


