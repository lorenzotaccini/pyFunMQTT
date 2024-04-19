from abc import ABC, abstractmethod
from typing import Any


class Service(ABC):

    @abstractmethod
    def serve(self, data: Any) -> Any:
        ...


class Split(Service):
    def serve(self, data: str):
        return list(data)


class Merge(Service):
    def serve(self, data: Any):
        print(data)


class Upper(Service):
    def serve(self, data: Any):
        return str(data).upper()
