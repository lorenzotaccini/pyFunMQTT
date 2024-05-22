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

# input: list of dict, output: dict(outtopic: payload)
class Split(Service):
    def serve(self, conf: dict, data: Any) -> dict:
        res = {}
        for t in conf['outTopic']:
            pass


class Upper(Service):
    def serve(self, conf, data: str):
        return str(data).upper()


class Extract(Service):
    def serve(self, conf, data: Any):
        pass
