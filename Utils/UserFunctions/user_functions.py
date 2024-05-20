from abc import ABC, abstractmethod
from typing import Any


class Service(ABC):
    @abstractmethod
    def serve(self, data: Any) -> Any:
        ...


# USER DEFINED CLASSES

class RemoveWS(Service):
    def serve(self, data: str):
        return data.replace(' ', '')


class Merge(Service):
    def serve(self, data: Any):
        print(data)


class Upper(Service):
    def serve(self, data: str):
        return str(data).upper()


class Extract(Service):
    def serve(self, data: Any):
        pass
